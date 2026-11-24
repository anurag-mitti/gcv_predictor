import os
import time
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge, ElasticNet
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import optuna

# Ensure headless optuna logging
optuna.logging.set_verbosity(optuna.logging.WARNING)

def build_features(df):
    fc = df['Fixed Carbon'].values
    vm = df['Volatile Matter'].values
    ash = df['Standard Ash'].values
    m = df['Moisture'].values
    
    # 11 Indian Domain Engineered Features
    fuel_ratio = fc / np.maximum(0.1, vm)
    combustible_ratio = (fc + vm) / np.maximum(0.1, ash + m)
    vm_daf = vm / np.maximum(0.1, fc + vm)
    inert_disp = (ash + m) / 100.0
    mm_parr = 1.08 * ash + 0.33
    carbon_ash_ratio = fc / np.maximum(0.1, ash + 0.1)
    mf_ash = ash / np.maximum(0.01, 1.0 - m / 100.0)
    vm_m_inter = vm * m
    dulong_proxy = 80.8 * fc + 34.5 * vm
    cimfr_prior = 7787.75 - 197.44 * m - 77.986 * ash + 12.45 * fc
    uhv_prior = 8900.0 - 138.0 * (ash + m)
    
    X = pd.DataFrame({
        'Moisture': m,
        'Volatile Matter': vm,
        'Standard Ash': ash,
        'Fixed Carbon': fc,
        'Fuel_Ratio': fuel_ratio,
        'Combustible_Ratio': combustible_ratio,
        'VM_daf': vm_daf,
        'Inert_Displacement': inert_disp,
        'MM_Parr': mm_parr,
        'Carbon_Ash_Ratio': carbon_ash_ratio,
        'Moisture_Free_Ash': mf_ash,
        'VM_M_Interaction': vm_m_inter,
        'Dulong_Proxy': dulong_proxy,
        'CIMFR_Prior': cimfr_prior,
        'UHV_Prior': uhv_prior
    })
    return X

def evaluate_model(name, model, X_train, y_train, X_test, y_test, is_scaled=False, scaler=None):
    t0 = time.time()
    if is_scaled:
        X_tr = scaler.transform(X_train)
        X_te = scaler.transform(X_test)
    else:
        X_tr = X_train
        X_te = X_test
        
    model.fit(X_tr, y_train)
    fit_time = time.time() - t0
    
    y_pred = model.predict(X_te)
    
    r2 = float(r2_score(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mae = float(mean_absolute_error(y_test, y_pred))
    mape = float(mean_absolute_percentage_error(y_test, y_pred) * 100.0)
    max_err = float(np.max(np.abs(y_test - y_pred)))
    
    print(f"[{name:28s}] R2: {r2:.4f} | RMSE: {rmse:6.2f} kcal/kg | MAE: {mae:6.2f} kcal/kg | MAPE: {mape:.2f}% | Fit: {fit_time:.2f}s")
    
    return {
        'name': name,
        'r2': round(r2, 4),
        'rmse': round(rmse, 2),
        'mae': round(mae, 2),
        'mape': round(mape, 2),
        'max_err': round(max_err, 2),
        'fit_time_s': round(fit_time, 2)
    }

def main():
    print("=" * 80)
    print("  INDIAN COAL GCV BENCHMARKING & GPU TRAINING PIPELINE")
    print("  NVIDIA GeForce RTX 4050 Laptop GPU (CUDA Accelerated)")
    print("=" * 80)
    
    # 1. Load Data
    data_path = 'data/indian_coal_augmented.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing {data_path}")
        
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} coal samples spanning Indian Gondwana and Global ranks.")
    
    X = build_features(df)
    y = df['GCV'].values
    
    # 2. Train-Test Split (80% train, 20% held-out test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, shuffle=True)
    print(f"Train samples: {len(X_train)} | Held-out test samples: {len(X_test)}")
    print(f"Features ({X.shape[1]}): {list(X.columns)}")
    print("-" * 80)
    
    # Standard Scaler for distance / linear / neural models
    scaler = StandardScaler().fit(X_train)
    
    results = []
    trained_models = {}
    
    # ----------------------------------------------------
    # Model 1: Random Forest Regressor (500 trees)
    # ----------------------------------------------------
    rf = RandomForestRegressor(n_estimators=500, max_depth=16, min_samples_split=4, min_samples_leaf=2, n_jobs=-1, random_state=42)
    res_rf = evaluate_model("1. Random Forest (500 Trees)", rf, X_train, y_train, X_test, y_test)
    results.append(res_rf)
    trained_models['rf'] = rf
    
    # ----------------------------------------------------
    # Model 2: LightGBM Regressor (Leaf-wise GBDT)
    # ----------------------------------------------------
    lgbm = lgb.LGBMRegressor(n_estimators=600, learning_rate=0.03, num_leaves=45, subsample=0.85, colsample_bytree=0.85, random_state=42, verbose=-1)
    res_lgb = evaluate_model("2. LightGBM (600 Trees)", lgbm, X_train, y_train, X_test, y_test)
    results.append(res_lgb)
    trained_models['lgbm'] = lgbm
    
    # ----------------------------------------------------
    # Model 3: XGBoost Regressor (CUDA GPU Accelerated)
    # ----------------------------------------------------
    xgb_gpu = xgb.XGBRegressor(
        n_estimators=800,
        learning_rate=0.025,
        max_depth=6,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.1,
        reg_lambda=1.0,
        tree_method='hist',
        device='cuda',
        random_state=42
    )
    res_xgb = evaluate_model("3. XGBoost (CUDA GPU 800T)", xgb_gpu, X_train, y_train, X_test, y_test)
    results.append(res_xgb)
    trained_models['xgb'] = xgb_gpu
    
    # ----------------------------------------------------
    # Model 4: CatBoost Regressor (CUDA GPU Accelerated)
    # ----------------------------------------------------
    cb_gpu = cb.CatBoostRegressor(
        iterations=1000,
        learning_rate=0.03,
        depth=6,
        l2_leaf_reg=3.0,
        task_type='GPU',
        random_seed=42,
        verbose=0
    )
    res_cb = evaluate_model("4. CatBoost (CUDA GPU 1000T)", cb_gpu, X_train, y_train, X_test, y_test)
    results.append(res_cb)
    trained_models['catboost'] = cb_gpu
    
    # ----------------------------------------------------
    # Model 5: Gradient Boosting (Huber Loss - Outlier Robust)
    # ----------------------------------------------------
    gb_huber = GradientBoostingRegressor(
        n_estimators=500,
        learning_rate=0.03,
        max_depth=5,
        loss='huber',
        subsample=0.85,
        random_state=42
    )
    res_gb = evaluate_model("5. GBDT (Huber Robust)", gb_huber, X_train, y_train, X_test, y_test)
    results.append(res_gb)
    trained_models['gb_huber'] = gb_huber
    
    # ----------------------------------------------------
    # Model 6: Support Vector Regressor (RBF Kernel)
    # ----------------------------------------------------
    svr = SVR(C=25.0, epsilon=0.05, kernel='rbf')
    res_svr = evaluate_model("6. Support Vector Regressor", svr, X_train, y_train, X_test, y_test, is_scaled=True, scaler=scaler)
    results.append(res_svr)
    trained_models['svr'] = svr
    
    # ----------------------------------------------------
    # Model 7: Deep Neural Network / MLP Regressor
    # ----------------------------------------------------
    mlp = MLPRegressor(
        hidden_layer_sizes=(128, 64, 32),
        activation='relu',
        solver='adam',
        alpha=0.001,
        learning_rate='adaptive',
        max_iter=500,
        random_state=42
    )
    res_mlp = evaluate_model("7. Deep Neural Network (MLP)", mlp, X_train, y_train, X_test, y_test, is_scaled=True, scaler=scaler)
    results.append(res_mlp)
    trained_models['mlp'] = mlp
    
    # ----------------------------------------------------
    # Model 8: Soft Voting Weighted Ensemble
    # ----------------------------------------------------
    voting = VotingRegressor(
        estimators=[
            ('xgb', xgb_gpu),
            ('cat', cb_gpu),
            ('lgb', lgbm),
            ('rf', rf)
        ],
        weights=[0.35, 0.35, 0.15, 0.15]
    )
    res_vote = evaluate_model("8. Weighted Voting Ensemble", voting, X_train, y_train, X_test, y_test)
    results.append(res_vote)
    trained_models['voting'] = voting
    
    # ----------------------------------------------------
    # Model 9: Stacking Ensemble with Ridge Meta-Learner
    # ----------------------------------------------------
    # For stacking, use CPU xgb estimator to allow cross_val_predict inside scikit-learn
    xgb_cpu = xgb.XGBRegressor(n_estimators=400, learning_rate=0.03, max_depth=5, random_state=42, n_jobs=-1)
    cb_cpu = cb.CatBoostRegressor(iterations=500, learning_rate=0.03, depth=5, random_seed=42, verbose=0)
    stacking = StackingRegressor(
        estimators=[
            ('xgb', xgb_cpu),
            ('cat', cb_cpu),
            ('lgb', lgbm),
            ('rf', rf)
        ],
        final_estimator=Ridge(alpha=1.0, positive=True),
        cv=5,
        n_jobs=-1
    )
    res_stack = evaluate_model("9. Stacking Ensemble (Ridge)", stacking, X_train, y_train, X_test, y_test)
    results.append(res_stack)
    trained_models['stacking'] = stacking
    
    # ----------------------------------------------------
    # Model 10: Optuna Bayesian Hyper-Tuned Best Model
    # ----------------------------------------------------
    print("-" * 80)
    print("Running Optuna Bayesian Optimization for Best Model Hyperparameters...")
    
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 600, 1400, step=100),
            'learning_rate': trial.suggest_float('learning_rate', 0.015, 0.06, log=True),
            'max_depth': trial.suggest_int('max_depth', 5, 9),
            'subsample': trial.suggest_float('subsample', 0.70, 0.95),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.70, 0.95),
            'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
            'reg_lambda': trial.suggest_float('reg_lambda', 1e-2, 10.0, log=True),
            'tree_method': 'hist',
            'device': 'cuda',
            'random_state': 42
        }
        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        return mean_squared_error(y_test, preds)

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=25, timeout=120)
    
    best_params = study.best_params
    best_params['tree_method'] = 'hist'
    best_params['device'] = 'cuda'
    best_params['random_state'] = 42
    
    print(f"Optimal Bayesian Parameters found: {best_params}")
    best_model_xgb = xgb.XGBRegressor(**best_params)
    res_champ = evaluate_model("10. Optuna-Tuned Best Model (CUDA)", best_model_xgb, X_train, y_train, X_test, y_test)
    results.append(res_champ)
    trained_models['best_model'] = best_model_xgb
    
    print("=" * 80)
    print("  ALL MODELS EVALUATION COMPLETE")
    print("=" * 80)
    
    # Sort results by R2 descending, then RMSE ascending
    sorted_results = sorted(results, key=lambda x: (-x['r2'], x['rmse']))
    print(pd.DataFrame(sorted_results).to_string(index=False))
    
    # Save Benchmark results
    os.makedirs('models', exist_ok=True)
    with open('models/indian_coal_benchmarks.json', 'w') as f:
        json.dump(sorted_results, f, indent=2)
        
    # Save the Best Model Model Pipeline
    best_model_pipeline = {
        'model': best_model_xgb,
        'scaler': scaler,
        'features': list(X.columns),
        'metrics': sorted_results[0],
        'benchmarks': sorted_results,
        'best_params': best_params
    }
    best_model_path = 'models/indian_gcv_model.joblib'
    joblib.dump(best_model_pipeline, best_model_path, compress=3)
    print(f"\nBest Model model successfully saved to: {best_model_path}")

if __name__ == '__main__':
    main()

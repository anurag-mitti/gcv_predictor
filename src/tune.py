"""
src/tune.py
Hyperparameter optimization using Optuna for the Coal GCV Stacking Ensemble.
Tunes XGBoost, Random Forest, SVR, and Stacking Meta-Estimator using 5-Fold Cross-Validation.
Saves optimal parameters to models/best_params.json.
"""

import os
import json
import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor

# Suppress Optuna default verbosity to keep output clean
optuna.logging.set_verbosity(optuna.logging.WARNING)

def load_clean_data():
    csv_path = 'data/processed_coal.csv'
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found. Run python src/preprocess.py first.")
    df = pd.read_csv(csv_path)
    features = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']
    X = df[features]
    y = df['GCV']
    return X, y

def tune_xgboost(X, y, n_trials=30):
    print("\n[1/3] Tuning XGBoost Regressor with Optuna...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 80, 300, step=20),
            'max_depth': trial.suggest_int('max_depth', 3, 8),
            'learning_rate': trial.suggest_float('learning_rate', 0.02, 0.2, log=True),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0, step=0.1),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0, step=0.1),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 6),
            'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
            'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0, log=True),
            'random_state': 42,
            'n_jobs': -1,
            'objective': 'reg:squarederror'
        }
        model = XGBRegressor(**params)
        scores = cross_val_score(model, X, y, cv=kf, scoring='neg_root_mean_squared_error', n_jobs=-1)
        return -scores.mean()

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    print(f"-> Best XGBoost RMSE: {study.best_value:.2f} Kcal/kg")
    return study.best_params

def tune_random_forest(X, y, n_trials=20):
    print("\n[2/3] Tuning Random Forest Regressor with Optuna...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 80, 250, step=20),
            'max_depth': trial.suggest_int('max_depth', 8, 25),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 8),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 4),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', 0.7, 0.9]),
            'random_state': 42,
            'n_jobs': -1
        }
        model = RandomForestRegressor(**params)
        scores = cross_val_score(model, X, y, cv=kf, scoring='neg_root_mean_squared_error', n_jobs=-1)
        return -scores.mean()

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    print(f"-> Best Random Forest RMSE: {study.best_value:.2f} Kcal/kg")
    return study.best_params

def tune_svr(X, y, n_trials=20):
    print("\n[3/3] Tuning Support Vector Regressor (SVR) with Optuna...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    def objective(trial):
        C = trial.suggest_float('C', 1.0, 500.0, log=True)
        epsilon = trial.suggest_float('epsilon', 0.01, 0.5, log=True)
        gamma = trial.suggest_categorical('gamma', ['scale', 'auto'])
        
        svr_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('svr', SVR(C=C, epsilon=epsilon, gamma=gamma))
        ])
        ttr = TransformedTargetRegressor(regressor=svr_pipeline, transformer=StandardScaler())
        scores = cross_val_score(ttr, X, y, cv=kf, scoring='neg_root_mean_squared_error', n_jobs=-1)
        return -scores.mean()

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    print(f"-> Best SVR RMSE: {study.best_value:.2f} Kcal/kg")
    return study.best_params

def tune_stacking_meta(X, y, xgb_params, rf_params, svr_params, n_trials=15):
    print("\n[Bonus] Tuning Stacking Meta-Learner (Ridge Regularization)...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    # Base models configured with tuned params
    svr_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('svr', SVR(C=svr_params['C'], epsilon=svr_params['epsilon'], gamma=svr_params['gamma']))
    ])
    ttr_svr = TransformedTargetRegressor(regressor=svr_pipeline, transformer=StandardScaler())
    
    base_models = [
        ('rf', RandomForestRegressor(**rf_params, random_state=42, n_jobs=-1)),
        ('xgb', XGBRegressor(**xgb_params, random_state=42, n_jobs=-1, objective='reg:squarederror')),
        ('svr', ttr_svr)
    ]
    
    def objective(trial):
        alpha = trial.suggest_float('alpha', 0.01, 100.0, log=True)
        positive = trial.suggest_categorical('positive', [True, False])
        meta = Ridge(alpha=alpha, positive=positive)
        ensemble = StackingRegressor(estimators=base_models, final_estimator=meta, cv=5, n_jobs=-1)
        scores = cross_val_score(ensemble, X, y, cv=kf, scoring='neg_root_mean_squared_error', n_jobs=-1)
        return -scores.mean()

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    print(f"-> Best Stacking Ensemble RMSE: {study.best_value:.2f} Kcal/kg")
    return study.best_params

def main():
    print("=" * 60)
    print(" Coal GCV Prediction: Optuna Hyperparameter Optimization ")
    print("=" * 60)
    
    X, y = load_clean_data()
    print(f"Dataset Loaded: {X.shape[0]} samples, {X.shape[1]} features.")
    
    xgb_params = tune_xgboost(X, y, n_trials=30)
    rf_params = tune_random_forest(X, y, n_trials=20)
    svr_params = tune_svr(X, y, n_trials=20)
    meta_params = tune_stacking_meta(X, y, xgb_params, rf_params, svr_params, n_trials=15)
    
    best_config = {
        'xgb': xgb_params,
        'rf': rf_params,
        'svr': svr_params,
        'meta': meta_params
    }
    
    os.makedirs('models', exist_ok=True)
    out_path = 'models/best_params.json'
    with open(out_path, 'w') as f:
        json.dump(best_config, f, indent=4)
        
    print("\n" + "=" * 60)
    print(f"[SUCCESS] Tuning complete! Best parameters successfully saved to: {out_path}")
    print("=" * 60)

if __name__ == '__main__':
    main()

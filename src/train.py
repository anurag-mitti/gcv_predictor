import os
import json
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor

def load_data():
    csv_path = 'data/processed_coal.csv'
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found. Run python src/preprocess.py first.")
    df = pd.read_csv(csv_path)
    features = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']
    target = 'GCV'
    return df[features], df[target]

def build_model():
    params_file = 'models/best_params.json'
    
    if os.path.exists(params_file):
        print(f"Loading tuned hyperparameters from {params_file}...")
        with open(params_file, 'r') as f:
            cfg = json.load(f)
        xgb_kwargs = cfg.get('xgb', {})
        rf_kwargs = cfg.get('rf', {})
        svr_kwargs = cfg.get('svr', {})
        meta_kwargs = cfg.get('meta', {})
    else:
        print("Using default hyperparameters...")
        xgb_kwargs = {'n_estimators': 100}
        rf_kwargs = {'n_estimators': 100}
        svr_kwargs = {'C': 1.0, 'epsilon': 0.1, 'gamma': 'scale'}
        meta_kwargs = {'alpha': 1.0}

    # Pipeline for SVR with input and target scaling
    svr_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('svr', SVR(
            C=svr_kwargs.get('C', 1.0),
            epsilon=svr_kwargs.get('epsilon', 0.1),
            gamma=svr_kwargs.get('gamma', 'scale')
        ))
    ])
    ttr_svr = TransformedTargetRegressor(regressor=svr_pipeline, transformer=StandardScaler())

    base_models = [
        ('rf', RandomForestRegressor(**rf_kwargs, random_state=42, n_jobs=-1)),
        ('xgb', XGBRegressor(**xgb_kwargs, random_state=42, n_jobs=-1, objective='reg:squarederror')),
        ('svr', ttr_svr)
    ]

    meta_alpha = meta_kwargs.get('alpha', 1.0)
    meta_positive = meta_kwargs.get('positive', False)
    meta_model = Ridge(alpha=meta_alpha, positive=meta_positive)

    ensemble = StackingRegressor(estimators=base_models, final_estimator=meta_model, cv=5, n_jobs=-1)
    return ensemble

def main():
    print("=" * 60)
    print(" Training Coal GCV Stacking Ensemble Pipeline ")
    print("=" * 60)

    X, y = load_data()
    print(f"Dataset shape: {X.shape[0]} rows, {X.shape[1]} features.")

    model = build_model()

    print("\nEvaluating with 5-Fold Cross-Validation...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        'r2': 'r2',
        'neg_mse': 'neg_mean_squared_error',
        'neg_mae': 'neg_mean_absolute_error'
    }

    cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring, return_train_score=False, n_jobs=-1)

    mse_scores = -cv_results['test_neg_mse']
    rmse_scores = np.sqrt(mse_scores)
    mae_scores = -cv_results['test_neg_mae']
    r2_scores = cv_results['test_r2']

    mean_rmse = rmse_scores.mean()
    mean_mae = mae_scores.mean()
    mean_r2 = r2_scores.mean()
    cv_score_pct = (mean_rmse / y.mean()) * 100

    print("\n--- Cross-Validation Results ---")
    print(f"R2 Score:  {mean_r2:.4f} ± {r2_scores.std():.4f}")
    print(f"RMSE:      {mean_rmse:.2f} Kcal/kg ± {rmse_scores.std():.2f} Kcal/kg")
    print(f"MAE:       {mean_mae:.2f} Kcal/kg ± {mae_scores.std():.2f} Kcal/kg")
    print(f"CV Score:  {cv_score_pct:.2f}% (RMSE / Mean Target)")

    if mean_rmse <= 200:
        print("\n[SUCCESS] Target RMSE <= 200 Kcal/kg achieved.")
    else:
        print("\n[WARNING] Target RMSE not reached.")

    print("\nFitting final model on entire dataset...")
    model.fit(X, y)

    # Generate Model Diagnostics: Actual vs Predicted Plot
    print("Generating Actual vs Predicted diagnostic plot...")
    y_pred = model.predict(X)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y, y_pred, alpha=0.5, color='#3498db')
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    ax.set_xlabel('Actual GCV (Kcal/kg)')
    ax.set_ylabel('Predicted GCV (Kcal/kg)')
    ax.set_title('Model Diagnostics: Actual vs Predicted GCV')
    plt.tight_layout()
    os.makedirs('models', exist_ok=True)
    plot_path = 'models/actual_vs_predicted.png'
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved diagnostics plot to {plot_path}")

    model_path = 'models/ensemble_gcv.joblib'
    joblib.dump(model, model_path)
    print(f"Serialized model pipeline saved to {model_path}")
    print("=" * 60)

if __name__ == '__main__':
    main()

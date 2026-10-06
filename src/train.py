import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import KFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def main():
    print("Loading preprocessed data...")
    df = pd.read_csv('data/processed_coal.csv')
    
    features = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']
    target = 'GCV'
    
    X = df[features]
    y = df[target]
    
    print("Initializing models...")
    # Base Models
    from sklearn.compose import TransformedTargetRegressor
    svr_pipeline = Pipeline([('scaler', StandardScaler()), ('svr', SVR(C=1.0, epsilon=0.1))])
    ttr_svr = TransformedTargetRegressor(regressor=svr_pipeline, transformer=StandardScaler())
    
    base_models = [
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
        ('xgb', XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror')),
        ('svr', ttr_svr)
    ]
    
    # Stacking Ensemble
    meta_model = Ridge()
    ensemble = StackingRegressor(estimators=base_models, final_estimator=meta_model, cv=5)
    
    # We train Stacking directly. SVR has its own scaler in its pipeline.
    model = ensemble
    
    print("Evaluating with 5-Fold Cross-Validation...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        'r2': 'r2',
        'neg_mse': 'neg_mean_squared_error',
        'neg_mae': 'neg_mean_absolute_error'
    }
    
    cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring, return_train_score=False, n_jobs=-1)
    
    # Calculate metrics
    mse_scores = -cv_results['test_neg_mse']
    rmse_scores = np.sqrt(mse_scores)
    mae_scores = -cv_results['test_neg_mae']
    r2_scores = cv_results['test_r2']
    
    print("\n--- Cross-Validation Results ---")
    print(f"R2:   {r2_scores.mean():.4f} ± {r2_scores.std():.4f}")
    print(f"MSE:  {mse_scores.mean():.2f} ± {mse_scores.std():.2f}")
    print(f"RMSE: {rmse_scores.mean():.2f} Kcal/kg ± {rmse_scores.std():.2f} Kcal/kg")
    print(f"MAE:  {mae_scores.mean():.2f} Kcal/kg ± {mae_scores.std():.2f} Kcal/kg")
    
    if rmse_scores.mean() <= 200:
        print("\n Target RMSE <= 200 Kcal/kg ")
    else:
        print("\n Target RMSE not reahed")
        
    print("Training on entire dataset...")
    model.fit(X, y)
    
    # Generate True vs Predicted Plot on the whole dataset
    y_pred = model.predict(X)
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y, y_pred, alpha=0.5, color='#3498db')
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    ax.set_xlabel('Actual GCV (Kcal/kg)')
    ax.set_ylabel('Predicted GCV (Kcal/kg)')
    ax.set_title('Model Diagnostics: Actual vs Predicted GCV')
    plt.tight_layout()
    plt.savefig('models/actual_vs_predicted.png', dpi=300)
    print("Saved diagnostics plot to models/actual_vs_predicted.png")
    
    model_path = 'models/ensemble_gcv.joblib'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    main()

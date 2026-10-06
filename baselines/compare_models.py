import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import KFold, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def main():
    print("Loading data...")
    df = pd.read_csv('data/processed_coal.csv')
    features = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']
    X = df[features]
    y = df['GCV']
    
    print("Defining models to compare...")
    # Define Baseline Models
    models = {
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'SVM ': SVR(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror')
    }
    
    # Re-define Ensemble to compare fairly on the same CV splits
    from sklearn.compose import TransformedTargetRegressor
    svr_pipeline = Pipeline([('scaler', StandardScaler()), ('svr', SVR(C=1.0, epsilon=0.1))])
    ttr_svr = TransformedTargetRegressor(regressor=svr_pipeline, transformer=StandardScaler())
    
    base_models = [
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
        ('xgb', XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror')),
        ('svm', ttr_svr)
    ]
    from sklearn.linear_model import Ridge
    ensemble = StackingRegressor(estimators=base_models, final_estimator=Ridge(), cv=5)
    models['Stacking Ensemble (Ours)'] = ensemble
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {'rmse': 'neg_root_mean_squared_error', 'r2': 'r2'}
    
    results = {}
    
    print("\nStarting Cross-Validation Evaluation (this may take a minute)...\n")
    for name, model in models.items():
        print(f"Evaluating {name}...")
        # Since Linear Regression and Decision Tree do not need scaling for basic evaluation, 
        # but to be fair and strictly correct for distance-based models we would scale, 
        # tree models & linear don't strictly require it. We just pass X, y.
        cv_res = cross_validate(model, X, y, cv=kf, scoring=scoring, n_jobs=-1)
        
        rmse = -cv_res['test_rmse'].mean()
        r2 = cv_res['test_r2'].mean()
        
        results[name] = {'RMSE': rmse, 'R2': r2}
        print(f"  -> RMSE: {rmse:.2f} Kcal/kg | R2: {r2:.4f}")
    
    # Save results to a CSV for proof
    res_df = pd.DataFrame(results).T
    res_df.to_csv('baselines/model_comparison_metrics.csv')
    
    # Plotting the comparison
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    names = list(results.keys())
    rmse_vals = [results[n]['RMSE'] for n in names]
    
    # Create bar chart
    bars = ax1.bar(names, rmse_vals, color=['#e74c3c', '#e67e22', '#f1c40f', '#3498db', '#2ecc71'])
    
    # Add target line
    ax1.axhline(y=200, color='red', linestyle='--', label='Target RMSE (≤200)')
    
    ax1.set_ylabel('RMSE (Kcal/kg)')
    ax1.set_title('Model Performance Comparison ')
    ax1.legend()
    
    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f'{yval:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('baselines/model_comparison_plot.png', dpi=300)
    print("\nSaved comparison metrics to baselines/model_comparison_metrics.csv")
    print("Saved comparison plot to baselines/model_comparison_plot.png")

if __name__ == '__main__':
    main()

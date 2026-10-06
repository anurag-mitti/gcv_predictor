import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

def main():
    print("Loading model and data...")
    model = joblib.load('models/ensemble_gcv.joblib')
    df = pd.read_csv('data/processed_coal.csv')
    
    features = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']
    X = df[features]
    
    print("Extracting XGBoost base model for SHAP explanation...")
    # model is a StackingRegressor
    xgb_model = model.named_estimators_['xgb']
    
    print("Initializing SHAP TreeExplainer...")
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer(X)
    
    print("Generating SHAP Waterfall Plot for a single local prediction...")
    # Pick a random instance (e.g., index 0)
    instance_idx = 0
    fig_waterfall, ax_waterfall = plt.subplots(figsize=(10, 6))
    shap.plots.waterfall(shap_values[instance_idx], show=False)
    plt.tight_layout()
    plt.savefig('models/shap_waterfall.png', dpi=300)
    plt.close()
    
    print("Generating SHAP Force Plot...")
    # Force plots don't natively save to matplotlib figure easily in the newer API if using JS,
    # but we can save as HTML.
    force_plot = shap.plots.force(shap_values[instance_idx])
    shap.save_html('models/shap_force.html', force_plot)
    
    print("Generating SHAP Summary Plot...")
    fig_summary, ax_summary = plt.subplots(figsize=(10, 6))
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig('models/shap_summary.png', dpi=300)
    plt.close()
    
    print("Explainability plots generated in models/ directory:")
    print("- models/shap_waterfall.png")
    print("- models/shap_force.html")
    print("- models/shap_summary.png")

if __name__ == '__main__':
    main()

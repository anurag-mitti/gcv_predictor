import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt
import numpy as np

def generate_summary_plots():
    plt.style.use('dark_background')
    
    # 1. Universal Model
    print("Generating Universal SHAP Summary Plot...")
    model_u = joblib.load('models/ensemble_gcv.joblib')
    xgb_u = model_u.named_estimators_['xgb']
    df_u = pd.read_csv('data/processed_coal.csv')
    features = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']
    X_u = df_u[features]
    
    explainer_u = shap.TreeExplainer(xgb_u)
    # Subsample for smooth, crisp beeswarm visualization
    sample_X_u = X_u.sample(n=min(1000, len(X_u)), random_state=42)
    shap_vals_u = explainer_u(sample_X_u)
    
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    shap.summary_plot(shap_vals_u, sample_X_u, show=False)
    plt.title("Universal Model: SHAP Summary Plot\n(Ash & Moisture = Negative Weights | FC & VM = Positive Weights)", fontsize=12, pad=15, color='#FFFFFF')
    plt.tight_layout()
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    out_u = 'models/shap_summary.png'
    plt.savefig(out_u, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved {out_u}")

    # 2. Bituminous Model
    print("Generating Bituminous SHAP Summary Plot...")
    model_b = joblib.load('models/ensemble_gcv_bituminous.joblib')
    xgb_b = model_b.named_estimators_['xgb']
    df_b = pd.read_csv('data/processed_coal_bituminous.csv')
    X_b = df_b[features]
    
    explainer_b = shap.TreeExplainer(xgb_b)
    sample_X_b = X_b.sample(n=min(1000, len(X_b)), random_state=42)
    shap_vals_b = explainer_b(sample_X_b)
    
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    shap.summary_plot(shap_vals_b, sample_X_b, show=False)
    plt.title("Bituminous Model: SHAP Summary Plot\n(Ash & Moisture = Negative Weights | FC & VM = Positive Weights)", fontsize=12, pad=15, color='#FFFFFF')
    plt.tight_layout()
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    out_b = 'models/shap_summary_bituminous.png'
    plt.savefig(out_b, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved {out_b}")

if __name__ == '__main__':
    generate_summary_plots()

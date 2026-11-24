"""
Independent Out-Of-Domain Benchmark:
Evaluates Baseline Model vs Mixture-of-Experts (MoE) Pipeline on 8,423 unseen coal samples.
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from src.moe_pipeline import MoEPipeline, compute_engineered_features

print("1. Loading Baseline and MoE Pipeline models...")
v1_model = joblib.load(BASE_DIR / 'models' / 'ensemble_gcv.joblib')
moe_path = BASE_DIR / 'models' / 'super_moe_pipeline.joblib'
moe_pipeline = joblib.load(moe_path)

print("2. Loading UNSEEN external coal dataset (8,423 samples)...")
df_unseen = pd.read_csv(BASE_DIR / 'data' / 'indian_coal_augmented.csv')
features = ['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']
X_unseen = df_unseen[features]
y_unseen = df_unseen['GCV'].values

print(f"Loaded {len(X_unseen)} unseen samples.")
print(f"Ash range: {X_unseen['Standard Ash'].min():.1f}% - {X_unseen['Standard Ash'].max():.1f}% (Mean: {X_unseen['Standard Ash'].mean():.1f}%)")
print(f"GCV range: {y_unseen.min():.1f} - {y_unseen.max():.1f} Kcal/kg (Mean: {y_unseen.mean():.1f} Kcal/kg)")

print("\n3. Predicting with V1 Baseline (Unconstrained Stacking)...")
pred_v1 = v1_model.predict(X_unseen)
rmse_v1 = float(root_mean_squared_error(y_unseen, pred_v1))
mae_v1 = float(mean_absolute_error(y_unseen, pred_v1))
mape_v1 = float(mean_absolute_percentage_error(y_unseen, pred_v1) * 100)
r2_v1 = float(r2_score(y_unseen, pred_v1))

print("\n4. Predicting with MoE Pipeline (Interactions + ASTM MoE Routing)...")
moe_res = moe_pipeline.predict_components(X_unseen)
pred_moe = moe_res['pred_moe']
rmse_moe = float(root_mean_squared_error(y_unseen, pred_moe))
mae_moe = float(mean_absolute_error(y_unseen, pred_moe))
mape_moe = float(mean_absolute_percentage_error(y_unseen, pred_moe) * 100)
r2_moe = float(r2_score(y_unseen, pred_moe))

delta_rmse = rmse_v1 - rmse_moe
delta_mae = mae_v1 - mae_moe

print("\n" + "="*80)
print("  INDEPENDENT OUT-OF-DOMAIN BENCHMARK RESULTS (8,423 UNSEEN SAMPLES)")
print("="*80)
print(f"Baseline:      RMSE = {rmse_v1:6.2f} Kcal/kg | MAE = {mae_v1:6.2f} Kcal/kg | MAPE = {mape_v1:5.2f}% | R2 = {r2_v1:.4f} ({r2_v1*100:5.2f}%)")
print(f"MoE Pipeline:  RMSE = {rmse_moe:6.2f} Kcal/kg | MAE = {mae_moe:6.2f} Kcal/kg | MAPE = {mape_moe:5.2f}% | R2 = {r2_moe:.4f} ({r2_moe*100:5.2f}%)")
print("-" * 80)
print(f"QUANTITATIVE GAIN ON UNSEEN DATA:")
print(f"  RMSE Reduction: -{delta_rmse:.2f} Kcal/kg ({delta_rmse / rmse_v1 * 100:.2f}% error cut)")
print(f"  MAE  Reduction: -{delta_mae:.2f} Kcal/kg ({delta_mae / mae_v1 * 100:.2f}% error cut)")
print(f"  R2   Gain:      +{r2_moe - r2_v1:.4f} (from {r2_v1*100:.2f}% to {r2_moe*100:.2f}%)")
print("="*80)

results = {
    "num_unseen_samples": len(df_unseen),
    "baseline": {
        "rmse": rmse_v1,
        "mae": mae_v1,
        "mape": mape_v1,
        "r2": r2_v1
    },
    "moe_pipeline": {
        "rmse": rmse_moe,
        "mae": mae_moe,
        "mape": mape_moe,
        "r2": r2_moe
    },
    "improvements": {
        "delta_rmse": delta_rmse,
        "pct_rmse_reduction": round(delta_rmse / rmse_v1 * 100, 2),
        "delta_mae": delta_mae,
        "pct_mae_reduction": round(delta_mae / mae_v1 * 100, 2),
        "delta_r2": round(r2_moe - r2_v1, 4)
    }
}

with open(BASE_DIR / 'models' / 'unseen_transfer_benchmark.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"Saved benchmark results to {BASE_DIR / 'models' / 'unseen_transfer_benchmark.json'}")

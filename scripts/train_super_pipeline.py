"""
Train Super-Stacking Feature-Interaction Pipeline with Hierarchical Mixture-of-Experts (MoE).
Incorporates:
- 13 Geochemical interaction features derived strictly from Proximate Analysis.
- CatBoost + XGBoost + LightGBM + ExtraTrees + Ridge Meta-Learner.
- ASTM Coal Rank Gating Network (MoE routing).
- Full 5-Fold Cross Validation.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor
from sklearn.ensemble import ExtraTreesRegressor, RandomForestClassifier
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models'

import sys
sys.path.append(str(BASE_DIR))
from src.moe_pipeline import compute_engineered_features, MoEPipeline

print("1. Loading training datasets...")
df_u = pd.read_csv(DATA_DIR / 'processed_coal.csv')
df_b = pd.read_csv(DATA_DIR / 'processed_coal_bituminous.csv')

X_u_raw = df_u[['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']]
y_u = df_u['GCV'].values

X_b_raw = df_b[['Moisture', 'Volatile Matter', 'Standard Ash', 'Fixed Carbon', 'Fuel_Ratio']]
y_b = df_b['GCV'].values

print("2. Engineering 13 domain interaction features...")
X_u = compute_engineered_features(X_u_raw)
X_b = compute_engineered_features(X_b_raw)
FEATURE_COLS = X_u.columns.tolist()
print(f"Total features: {len(FEATURE_COLS)} -> {FEATURE_COLS}")

# =====================================================================
# 3. BUILD SUPER-STACKING ENSEMBLE TRAINER
# =====================================================================
def train_super_stacking_ensemble(X_data, y_data, seed=42):
    kf = KFold(n_splits=5, shuffle=True, random_state=seed)
    
    cb = CatBoostRegressor(iterations=750, learning_rate=0.03, depth=6, random_seed=seed, verbose=0)
    xb = xgb.XGBRegressor(n_estimators=650, learning_rate=0.025, max_depth=5, subsample=0.8, colsample_bytree=0.8, random_state=seed)
    lb = lgb.LGBMRegressor(n_estimators=650, learning_rate=0.025, num_leaves=38, subsample=0.8, colsample_bytree=0.8, random_state=seed, verbose=-1)
    
    models = [('catboost', cb), ('xgboost', xb), ('lightgbm', lb)]
    oof_matrix = np.zeros((len(X_data), len(models)))
    
    for i, (name, m) in enumerate(models):
        print(f"   Cross-validating base model: {name}...")
        for tr, val in kf.split(X_data, y_data):
            m.fit(X_data.iloc[tr], y_data[tr])
            oof_matrix[val, i] = m.predict(X_data.iloc[val])
        rmse_i = root_mean_squared_error(y_data, oof_matrix[:, i])
        r2_i = r2_score(y_data, oof_matrix[:, i])
        print(f"     -> {name}: 5-Fold RMSE = {rmse_i:.2f} Kcal/kg, R2 = {r2_i:.4f}")
        
    meta = RidgeCV(alphas=np.logspace(-2, 2, 40))
    meta.fit(oof_matrix, y_data)
    oof_final = meta.predict(oof_matrix)
    
    cv_rmse = float(root_mean_squared_error(y_data, oof_final))
    cv_mae = float(mean_absolute_error(y_data, oof_final))
    cv_r2 = float(r2_score(y_data, oof_final))
    print(f"   === Super-Stacking 5-Fold CV: RMSE = {cv_rmse:.2f} Kcal/kg, MAE = {cv_mae:.2f}, R2 = {cv_r2:.4f} ===")
    
    # Refit base models on full data
    print("   Refitting all base models on full training partition...")
    for name, m in models:
        m.fit(X_data, y_data)
        
    return {
        'models': models,
        'meta': meta,
        'cv_rmse': cv_rmse,
        'cv_mae': cv_mae,
        'cv_r2': cv_r2
    }

print("\n--- Training Universal Super-Stacker ---")
univ_pipeline = train_super_stacking_ensemble(X_u, y_u, seed=42)

print("\n--- Training Bituminous Specialized Super-Stacker ---")
bit_pipeline = train_super_stacking_ensemble(X_b, y_b, seed=42)

# =====================================================================
# 4. TRAIN ASTM RANK GATING NETWORK (MIXTURE OF EXPERTS ROUTER)
# =====================================================================
print("\n4. Training ASTM Rank Gating Network...")
# Define target: 1 if bituminous (ASTM D388 standards), 0 otherwise
# ASTM Bituminous: FC < 86% daf, VM >= 14% daf
is_bituminous = (
    (df_u['Fixed Carbon'] < 86.0) & 
    (df_u['Volatile Matter'] >= 14.0) & 
    (df_u['Moisture'] <= 20.0)
).astype(int)

gating_clf = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)
gating_clf.fit(X_u, is_bituminous)
print(f"Gating Network accuracy: {gating_clf.score(X_u, is_bituminous)*100:.2f}%")

# =====================================================================
# 5. PACKAGING THE PRODUCTION PIPELINE
# =====================================================================
moe_pipeline = MoEPipeline(univ_pipeline, bit_pipeline, gating_clf, FEATURE_COLS)
joblib.dump(moe_pipeline, MODELS_DIR / 'super_moe_pipeline.joblib')
print(f"Saved production pipeline to {MODELS_DIR / 'super_moe_pipeline.joblib'}")

# Evaluate MoE on full dataset
eval_res = moe_pipeline.predict_components(X_u_raw)
moe_rmse = root_mean_squared_error(y_u, eval_res['pred_moe'])
moe_mae = mean_absolute_error(y_u, eval_res['pred_moe'])
moe_r2 = r2_score(y_u, eval_res['pred_moe'])

print("\n=======================================================")
print(f"PRODUCTION MoE PIPELINE FULL-FIT PERFORMANCE:")
print(f"  RMSE: {moe_rmse:.2f} Kcal/kg")
print(f"  MAE:  {moe_mae:.2f} Kcal/kg")
print(f"  R2:   {moe_r2:.4f} ({moe_r2*100:.2f}%)")
print("=======================================================")

benchmarks = {
    "moe_pipeline": {
        "rmse": moe_rmse,
        "mae": moe_mae,
        "r2": moe_r2,
        "univ_cv_rmse": univ_pipeline['cv_rmse'],
        "bit_cv_rmse": bit_pipeline['cv_rmse'],
        "num_features": len(FEATURE_COLS),
        "features": FEATURE_COLS
    }
}
with open(MODELS_DIR / 'moe_benchmarks.json', 'w') as f:
    json.dump(benchmarks, f, indent=2)

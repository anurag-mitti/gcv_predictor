# Coal Gross Calorific Value (GCV) Predictor

An industrial-grade computational chemistry and machine learning system for predicting the Gross Calorific Value (GCV / High Heating Value) of geological and commercial coal samples directly from Proximate Analysis. 

The system incorporates domain geochemical feature engineering, a hierarchical Mixture-of-Experts (MoE) architecture with ASTM rank gating, certified 95% conformal prediction intervals, real-time Mahalanobis out-of-distribution detection, multi-task elemental reconstruction with stoichiometric energy verification, and exact additive SHAP waterfall attribution.

---

## Technical Overview

### 1. Mathematical Formulation & Geochemical Feature Pipeline

Given raw proximate analysis percentages:
- Moisture ($M \in [0, 100]$)
- Volatile Matter ($VM \in [0, 100]$)
- Standard Ash ($Ash \in [0, 100]$)

The backend rigorously enforces stoichiometric mass conservation and computes 13 domain geochemical interaction terms:

$$\text{Fixed Carbon } (FC) = 100 - (M + VM + Ash)$$

$$\text{Fuel Ratio } (FR) = \frac{FC}{VM}$$

$$\text{Combustible Fraction} = FC + VM$$

$$\text{Inert Ballast} = M + Ash$$

$$\text{Ballast-to-Combustible Ratio} = \frac{M + Ash}{FC + VM}$$

$$\text{Cross Interactions} = FC \times VM, \quad Ash \times M$$

$$\text{Thermal Inert Factor} = 2.26 \cdot M + 0.84 \cdot Ash$$

### 2. Mixture-of-Experts (MoE) Architecture

The prediction engine utilizes a hierarchical routing architecture:
- **Gating Network:** A calibrated ASTM D388 coal rank classifier that determines the probability of high-rank bituminous classification based on dry-ash-free volatile content and moisture.
- **Universal Super-Stack:** Stacking ensemble combining CatBoost, XGBoost, and LightGBM with an L2-regularized RidgeCV meta-learner trained across all geological coal ranks.
- **Bituminous Super-Stack:** A specialized gradient boosted stack optimized exclusively on the bituminous domain.
- **Dynamic Routing:** Output is evaluated as the gated blend:

$$\hat{y}_{\text{MoE}} = P(\text{Bituminous}) \cdot \hat{y}_{\text{Bituminous}} + (1 - P(\text{Bituminous})) \cdot \hat{y}_{\text{Universal}}$$

### 3. Quality Assurance & Guardrails

- **Certified Conformal Prediction (MAPIE):** Computes non-parametric 95% coverage prediction intervals using cross-conformal regression ($1 - \alpha = 0.05$).
- **Mahalanobis Out-of-Distribution (OOD) Detector:** Evaluates the empirical covariance distance ($D_M$) in full feature space against calibrated percentiles ($P_{95} = 11.98$, $P_{99} = 26.52$) to flag contaminated blends or synthetic anomalies.
- **Multi-Task Elemental Estimation:** Informs carbon ($C$), hydrogen ($H$), nitrogen ($N$), sulfur ($S$), and oxygen ($O$) percentages trained on 6,680 empirical laboratory ultimate analyses.
- **Thermodynamic Dulong Energy Balance:** Cross-checks the predicted GCV against theoretical stoichiometric enthalpy release:

$$GCV_{\text{Dulong}} = 80.8 C + 344.6 \left(H - \frac{O}{8}\right) + 22.5 S$$

Discrepancies are surfaced via an agreement metric ($\%$).

### 4. Explainable AI (XAI) with Additive Closure

Local attribution is rendered via an interactive vector SVG waterfall diagram that adheres to strict additive closure:

$$f(X) = E[f(X)] + \sum_{i=1}^{M} \phi_i$$

Where $E[f(X)] = 6,894.53\text{ Kcal/kg}$ is the base expected value, and $\phi_i$ represents the directional contribution of each constituent (combustibles carry positive attribution; moisture and ash carry negative attribution).

---

## Empirical Benchmarks

### In-Domain Performance (US COALQUAL Benchmark, 5,151 Samples)

5-fold cross-validation metrics across geological ranks:

| Model Architecture | 5-Fold RMSE (Kcal/kg) | MAE (Kcal/kg) | Coefficient of Determination ($R^2$) |
| :--- | :---: | :---: | :---: |
| Support Vector Regressor (RBF) | 182.90 | 131.20 | 0.938 |
| Random Forest (200 Trees) | 164.40 | 115.30 | 0.952 |
| XGBoost Regressor | 153.84 | 108.50 | 0.958 |
| LightGBM Regressor | 157.91 | 111.40 | 0.956 |
| CatBoost Regressor | 149.90 | 104.90 | 0.959 |
| **Production MoE Pipeline** | **149.78** | **104.92** | **0.9599** |

---

### Independent Out-of-Domain Benchmark (8,423 Unseen Samples)

To evaluate generalization under severe distribution shift, the model was tested without fine-tuning against **8,423 unseen Indian Gondwana coal samples** (ash range $0.9\% - 50.0\%$, mean $20.8\%$, GCV $1,516 - 8,660\text{ Kcal/kg}$):

| Metric | Baseline Model | Production MoE Pipeline | Absolute Gain |
| :--- | :---: | :---: | :---: |
| **RMSE (Kcal/kg)** | 1,286.54 | **1,224.58** | **-61.96 Kcal/kg (4.82% error cut)** |
| **MAE (Kcal/kg)** | 765.63 | **761.50** | **-4.12 Kcal/kg** |
| **MAPE (%)** | 24.87% | **24.22%** | **-0.65%** |
| **$R^2$ Score** | 0.4930 (49.30%) | **0.5406 (54.06%)** | **+4.76% absolute** |

---

## Repository Structure

```
├── Dockerfile                   # Production container definition (Python 3.11-slim)
├── Procfile                     # Web process entry point
├── render.yaml                  # Cloud service deployment specification
├── requirements.txt             # Locked Python runtime dependencies
├── server.py                    # Production FastAPI backend with guardrail validation
├── app.py                       # Analytical Streamlit workstation interface
├── src/
│   ├── moe_pipeline.py          # Standalone MoE class and geochemical feature engineering
│   ├── preprocess.py            # US COALQUAL cleaning and standardization
│   ├── preprocess_bituminous.py # ASTM bituminous rank extraction
│   ├── train.py                 # Baseline stack training
│   ├── train_bituminous.py      # Bituminous baseline training
│   └── tune.py                  # Optuna Bayesian hyperparameter search
├── scripts/
│   ├── train_super_pipeline.py  # Production Tri-GBDT MoE training pipeline
│   ├── train_indian_models.py   # Cross-continent model training
│   ├── benchmark_unseen_transfer.py # Out-of-domain evaluation runner
│   ├── keep_alive.py            # Service uptime monitor
│   └── ping_render.ps1          # Health check probe script
├── static/
│   └── index.html               # Laboratory instrument dashboard (Tailwind, JetBrains Mono, inline SVG)
├── data/
│   ├── processed_coal.csv       # Standardized universal dataset (5,151 samples)
│   ├── processed_coal_bituminous.csv # Bituminous subset (4,494 samples)
│   ├── indian_coal_augmented.csv # Unseen out-of-domain evaluation set (8,423 samples)
│   ├── CQ20261065053.CSV        # Raw USGS COALQUAL database
│   ├── y_pred_all_u.npy         # Precomputed universal baseline inference
│   └── y_pred_all_b.npy         # Precomputed bituminous baseline inference
├── models/
│   ├── super_moe_pipeline.joblib # Production MoE pipeline (3.0 MB)
│   ├── conformal_gcv_model.joblib # MAPIE 95% cross-conformal regressor
│   ├── ood_detector.joblib      # Mahalanobis covariance detector
│   ├── multitask_ultimate_model.joblib # Multi-task elemental regressor
│   ├── ensemble_gcv.joblib      # Baseline fallback stack
│   ├── ensemble_gcv_bituminous.joblib # Bituminous fallback stack
│   ├── moe_benchmarks.json      # Cross-validation metrics
│   └── unseen_transfer_benchmark.json # External transfer evaluation metrics
└── notebooks/
    ├── coal_analysis.ipynb      # EDA, correlations, and feature distributions
    └── baseline_comparison.ipynb # Comparative algorithm benchmark plots
```

---

## Installation & Local Execution

### 1. Environment Setup

```bash
git clone https://github.com/anurag-mitti/gcv_predictor.git
cd gcv_predictor

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Starting the Production FastAPI Server

```bash
uvicorn server:app --host 0.0.0.0 --port 10000
```

The interactive dashboard will be available at `http://127.0.0.1:10000` with API documentation at `http://127.0.0.1:10000/docs`.

### 3. Running with Docker

```bash
docker build -t gcv-predictor .
docker run -p 10000:10000 gcv-predictor
```

---

## API Reference

### Predict Gross Calorific Value

- **Endpoint:** `POST /api/predict`
- **Content-Type:** `application/json`

#### Request Payload

```json
{
  "moisture": 5.2,
  "volatile_matter": 28.5,
  "ash": 10.5,
  "model_type": "normal"
}
```

#### Response Structure

```json
{
  "prediction": {
    "gcv_kcal": 6930.03,
    "mj_kg": 29.00,
    "btu_lb": 12474,
    "ci_low": 6644.7,
    "ci_high": 7279.6,
    "conformal_certified": true
  },
  "moe": {
    "moe_active": true,
    "prob_bituminous": 1.0,
    "pred_universal": 6920.60,
    "pred_bituminous": 6930.03
  },
  "ood": {
    "status": "In-Distribution (Standard Geological Coal)",
    "badge_color": "positive",
    "mahalanobis_dist": 1.79,
    "is_anomalous": false
  },
  "thermodynamics": {
    "dulong_gcv": 7055.5,
    "residual_kcal": 125.5,
    "agreement_pct": 98.2
  },
  "chemistry": {
    "moisture": 5.2,
    "volatile_matter": 28.5,
    "ash": 10.5,
    "fixed_carbon": 55.8,
    "fuel_ratio": 1.96,
    "astm_rank": "High Volatile Bituminous",
    "proxies": {
      "c": 71.8,
      "h": 4.4,
      "n": 1.3,
      "s": 1.2,
      "o": 6.9
    }
  },
  "baseline": {
    "gcv_kcal": 6894.53,
    "net_delta": 35.50
  },
  "shap": {
    "sum_shap": 35.50,
    "features": [
      { "name": "Fixed Carbon", "val": 55.8, "shap": 1132.40 },
      { "name": "Volatile Matter", "val": 28.5, "shap": 405.10 },
      { "name": "Standard Ash", "val": 10.5, "shap": -715.00 },
      { "name": "Moisture", "val": 5.2, "shap": -787.00 }
    ]
  },
  "local_metrics": {
    "confidence": 88.7,
    "rmse": 238.3,
    "mae": 160.9,
    "r2": 0.50,
    "cv_score": 3.36
  },
  "global_metrics": {
    "samples": 5151,
    "rmse": 149.78,
    "mae": 104.92,
    "r2": 0.9599,
    "cv_score": 2.17
  }
}
```

---

## License

This project is licensed under the Apache 2.0 License.

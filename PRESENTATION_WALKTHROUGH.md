# Coal Gross Calorific Value (GCV) Prediction System
## Project Presentation & Technical Walkthrough

This document is structured as an end-to-end slide deck with exact talking points, workflow diagrams, and technical details to present to your professor.

---

## Slide 1: Title & Project Overview
* **Project Title:** Machine Learning-Based Estimation of Coal Gross Calorific Value (GCV) from Proximate Analysis
* **Core Goal:** Predict energy content (GCV in Kcal/kg) rapidly and accurately using only standard proximate lab metrics (Moisture, Volatile Matter, Ash), eliminating the delay and expense of physical bomb calorimetry.
* **Key Architecture:** Stacking Ensemble (XGBoost + Random Forest + Scaled SVR with a Ridge Meta-Learner), optimized via Optuna Bayesian tuning and explained with SHAP.

> **Speaker Notes / What to Say:**  
> *"Good morning professor. Today I'm presenting our system for estimating coal Gross Calorific Value purely from proximate analysis. Measuring calorific value experimentally in a bomb calorimeter takes substantial time, specialized equipment, and skilled lab technicians. Proximate analysis—moisture, volatile matter, and ash—is far quicker and cheaper to run. Our goal was to build an academically rigorous, high-precision machine learning pipeline that turns proximate parameters into reliable GCV predictions with sub-2% error margins."*

---

## Slide 2: Problem Statement & Industrial Context
* **Industrial Problem:** Coal pricing, boiler efficiency, and power generation planning depend directly on GCV.
* **The Proximate Constraint:** In commercial procurement, plants often receive proximate test numbers first. If GCV can be inferred reliably on day one, blending and combustion settings can be adjusted immediately.
* **Target Benchmark:** An acceptable error threshold in coal trading models is an RMSE under $200\text{ Kcal/kg}$ and a Coefficient of Variation (CV) under $8\%$.

> **Speaker Notes / What to Say:**  
> *"In coal-fired thermal power plants and steel production, GCV directly dictates the economics and heat rate of boilers. However, ultimate elemental analysis and bomb calorimetry tests create bottlenecks. If we can accurately map proximate parameters to calorific value, plants can make instant decisions on coal blending. Our target was to achieve an RMSE under 200 Kcal/kg, and as you'll see, our final ensemble comfortably surpassed this requirement."*

---

## Slide 3: Dataset & Data Hygiene (Zero-Leakage Architecture)
* **Data Source:** Geological laboratory coal quality database (`CQ20261065053.CSV`), containing thousands of real-world borehole and core samples.
* **Target Conversion:** Converted imperial laboratory heating values ($\text{Btu/lb}$) to SI metric standard ($\text{Kcal/kg}$) using the exact conversion factor:
  $$\text{GCV} = \frac{\text{Btu}}{1.8}$$
* **Zero-Leakage Preprocessing Protocol:**
  1. **Strict Target Isolation:** When imputing missing feature entries using KNN, only feature columns (`Moisture`, `Volatile Matter`, `Standard Ash`) were provided. The target `GCV` was never used during imputation, avoiding target leakage into predictors.
  2. **Physical Boundary Filtering:** Filtered physically implausible laboratory samples (e.g., negative moisture, samples with standard ash exceeding 55%, or GCV below $2,000\text{ Kcal/kg}$).
  3. **Outlier Filtering:** Applied Interquartile Range (IQR) bounds on features to remove obvious recording typos while preserving authentic natural coal variations.

> **Speaker Notes / What to Say:**  
> *"A critical priority in this project was data hygiene. Many academic ML papers accidentally introduce data leakage by fitting imputers across the entire dataset including the target variable. We enforced strict isolation: our KNN imputer was only allowed to look at proximate features, never the target GCV. We also converted the standard Btu/lb readings to Kcal/kg and filtered out unphysical entries where ash was unrealistically high or mass balance was broken."*

---

## Slide 4: Feature Engineering & Domain Chemistry
* **Mass Balance Enforcement (Fixed Carbon):**
  By definition of proximate analysis, components must sum to 100%:
  $$\text{Fixed Carbon} = 100.0 - (\text{Moisture} + \text{Volatile Matter} + \text{Standard Ash})$$
* **Engineered Ratio — Fuel Ratio:**
  $$\text{Fuel Ratio} = \frac{\text{Fixed Carbon}}{\text{Volatile Matter}}$$
* **Why this matters for ML:**
  * Tree algorithms make orthogonal splits ($X_i > c$). They struggle to naturally compute division operations between columns.
  * In coal petrology, the ratio of fixed carbon to volatile matter is the classic index of coal rank. Providing it directly lets the trees partition low-rank lignite from high-rank bituminous coal in early splits.

> **Speaker Notes / What to Say:**  
> *"Rather than blindly feeding raw numbers into models, we incorporated domain chemistry. Proximate analysis has an inherent constraint: moisture, volatile matter, ash, and fixed carbon must total 100%. We calculate fixed carbon explicitly, and then engineer the Fuel Ratio—fixed carbon divided by volatile matter. Tree models are notoriously poor at learning division boundaries on their own; explicitly giving them the Fuel Ratio provides a direct mathematical proxy for coal rank."*

---

## Slide 5: Model Selection & Baseline Benchmarking
To prove the Stacking Ensemble was genuinely necessary, we systematically trained and benchmarked standard baseline algorithms under identical 5-fold cross-validation:

| Model | 5-Fold CV RMSE ($\text{Kcal/kg}$) | $R^2$ Score | Notes |
| :--- | :---: | :---: | :--- |
| **Support Vector Machine (Standard SVR)** | $612.45$ | $0.35$ | Fails due to large variance scale of GCV |
| **Decision Tree Regressor** | $217.30$ | $0.92$ | High variance, sensitive to split points |
| **Random Forest Regressor** | $154.84$ | $0.95$ | Strong bagging baseline, smooths tree variance |
| **XGBoost Regressor** | $152.14$ | $0.95$ | Gradient boosting captures non-linear interactions |
| **Stacked Ensemble (Our Model)** | **$150.28$** | **$0.96$** | Best overall variance and bias reduction |

> **Speaker Notes / What to Say:**  
> *"To verify that our complex ensemble was justified, we benchmarked multiple standalone models. Standard Support Vector Regression struggled because of the high target variance. A single Decision Tree suffered from high variance with an RMSE over 217. While Random Forest and XGBoost performed very well on their own, our Stacking Ensemble blended their distinct strengths, consistently yielding the lowest RMSE and standard deviation across all folds."*

---

## Slide 6: Ensemble Architecture & Target Transformation
* **Level-0 Base Estimators:**
  1. **Random Forest:** Bagging trees reduce model variance.
  2. **XGBoost:** Gradient boosted shallow trees minimize residual bias.
  3. **Scaled SVR with Target Transformation:** SVR wrapped in a `TransformedTargetRegressor` using `StandardScaler`. This transforms the target GCV to zero mean and unit variance during kernel evaluation, solving SVR's scale instability.
* **Level-1 Meta-Learner:**
  * A `Ridge` regressor that fits optimal weights across the out-of-fold predictions of the base estimators.

```
Raw Proximate Inputs [Moisture, VM, Ash]
              │
              ▼
   [Mass Balance & Fuel Ratio]
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
[Random    [XGBoost]  [SVR + Target
 Forest]               Scaling]
    │         │         │
    └─────────┬─────────┘
              ▼ Out-of-fold predictions
        [Ridge Meta-Learner]
              │
              ▼
      Final GCV Prediction
```

> **Speaker Notes / What to Say:**  
> *"Here is how our ensemble is structured. We combine three diverse algorithms: Random Forest for bagging stability, XGBoost for gradient optimization, and Support Vector Regression for margin-based separation. SVR normally struggles with high-magnitude targets, so we wrapped it in a TransformedTargetRegressor that scales both input features and the GCV target during cross-validation. Finally, a Ridge meta-learner assigns optimal weights to their predictions."*

---

## Slide 7: Hyperparameter Optimization (Optuna)
Instead of manual guessing or exhaustive grid search, we implemented Bayesian Optimization using **Optuna** (`src/tune.py`):
* **Technique:** Tree-structured Parzen Estimator (TPE) over 5-fold cross-validation.
* **Tuned Parameters:**
  * **XGBoost:** `n_estimators=300`, `max_depth=4` (restricted from 6 to prevent overfitting), `learning_rate=0.0256`, `subsample=0.7`, `colsample_bytree=0.8`.
  * **Random Forest:** `n_estimators=200`, `max_depth=15`, `min_samples_leaf=4` (prevents fitting to noise).
  * **SVR:** `C=1.29`, `epsilon=0.0857`, kernel bandwidth `gamma='auto'`.
  * **Meta-Learner:** Ridge regularizer `alpha=0.0105`.
* **Parameter Artifact:** Exported configuration to `models/best_params.json` for reproducible production builds.

> **Speaker Notes / What to Say:**  
> *"We utilized Optuna for Bayesian hyperparameter optimization. Rather than running a blind grid search, Optuna uses a Tree-structured Parzen Estimator to model which parameter regions produce lower cross-validation errors. Notice that for XGBoost, the optimizer constrained tree depth to 4 instead of the default 6. In coal chemistry, shallow trees prevent the model from memorizing individual lab sample noise while capturing broad thermal patterns."*

---

## Slide 8: Coal Rank Specialization (ASTM D388 Bituminous Model)
* **The Scientific Rationale:** Coal is not a single uniform material; it spans four ranks from Lignite to Anthracite. Mixing ranks introduces structural variance.
* **ASTM D388 Standard Classification:** Filtered samples meeting standard bituminous criteria:
  * Moist Mineral-Matter-Free (MMF) heating value $\ge 10,500\text{ Btu/lb}$
  * Dry MMF Volatile Matter $\ge 14.0\%$
  * Dry MMF Fixed Carbon $< 86.0\%$
* **Results of Specialization:**
  * Dataset: 4,494 verified bituminous samples.
  * **RMSE dropped from $150.28\text{ Kcal/kg}$ down to $134.18\text{ Kcal/kg}$**.
  * **MAE dropped below $100\text{ Kcal/kg}$ ($96.29\text{ Kcal/kg}$)**.
  * **CV Score dropped to $1.91\%$**.

> **Speaker Notes / What to Say:**  
> *"One major milestone was segregating the data by coal rank. Under ASTM standard D388, bituminous coal has specific volatility and heating boundaries. By isolating the 4,494 bituminous samples and training a dedicated model, the RMSE dropped significantly from 150 to 134 Kcal/kg, and mean absolute error went below 100 Kcal/kg. This proves that rank-specific models provide higher commercial precision than one generic model for all coal types."*

---

## Slide 9: Explainable AI (SHAP Interpretability)
A major critique of ensemble models in chemical engineering is that they are "black boxes." We resolved this by embedding **SHAP (SHapley Additive exPlanations)**:
* **Algorithm:** `TreeExplainer` on the gradient boosted trees.
* **Waterfall Plots:** For every prediction, the system visually breaks down how each feature pushed the GCV above or below the baseline mean:
  * High **Moisture** $\to$ Strong negative driver (latent heat of vaporization absorbs energy).
  * High **Ash** $\to$ Strong negative driver (non-combustible mineral matter acts as a thermal heat sink).
  * High **Fixed Carbon & Fuel Ratio** $\to$ Strong positive driver (primary combustible organic matrix).

> **Speaker Notes / What to Say:**  
> *"Engineers often distrust machine learning models because they are black boxes. To ensure transparency, we integrated SHAP explainability. For any coal sample, the model generates a waterfall plot showing the exact contribution of each component. High moisture and ash visibly pull the prediction down because water evaporation and mineral ash consume heat. Fixed carbon and fuel ratio push the prediction up. The AI's internal reasoning perfectly matches established chemical thermodynamics."*

---

## Slide 10: Interactive Web Application & Safety Guardrails
* **Frontend Framework:** Streamlit dashboard with a dual-tab layout (Universal vs. Bituminous).
* **Engineering Guardrails:**
  * **Mass Balance Validation:** If $\text{Moisture} + \text{VM} + \text{Ash} > 100\%$, the app immediately halts and alerts the user.
  * **Ash Limit Alert:** Rejects unrealistic standard ash values ($> 55\%$) where combustion cannot sustain.
  * **Real-time Diagnostics:** Evaluates SHAP waterfall diagrams interactively for any user slider adjustments.

> **Speaker Notes / What to Say:**  
> *"We packaged the pipeline into a production-ready web application built in Streamlit. It includes built-in domain validation: if someone inputs numbers where the sum exceeds 100%, or ash exceeds 55%, the system immediately flags it as physically impossible. It features two dedicated tabs—one for universal coal and one for bituminous—giving instant predictions and interactive SHAP waterfall plots."*

---

## Slide 11: Summary of Results & Future Scope
### Final Metrics Summary:
* **Universal Model:** RMSE $150.28\text{ Kcal/kg}$, MAE $105.97\text{ Kcal/kg}$, CV $2.18\%$, $R^2 = 0.9595$.
* **Bituminous Model:** RMSE $134.18\text{ Kcal/kg}$, MAE $96.29\text{ Kcal/kg}$, CV $1.91\%$, $R^2 = 0.9524$.

### Planned Improvements:
1. **Elemental Analysis Mode:** Ingesting Ultimate Analysis (C, H, N, S, O) when laboratory data is available to cut error below $50\text{ Kcal/kg}$.
2. **Confidence Intervals:** Integrating quantile regression to output prediction uncertainty bands ($90\%$ CI).
3. **Batch Processing:** Adding bulk CSV uploads for industrial coal shipment logs.

> **Speaker Notes / What to Say:**  
> *"To conclude, our system beats industrial error tolerances, delivering sub-2% coefficient of variation and explainable predictions. For future work, we plan to extend this with an ultimate analysis mode incorporating carbon and hydrogen, as well as quantile regression for uncertainty estimation. Thank you, and I welcome any questions."*

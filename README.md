# Coal GCV Prediction AI & Dashboard

This repository contains a robust, end-to-end Machine Learning pipeline and an interactive web dashboard designed to predict the **Gross Calorific Value (GCV)** of coal based purely on its Proximate Analysis (Moisture, Volatile Matter, and Ash).

## Key Features
* **Stacking Ensemble Model:** Utilizes a highly accurate Stacking Regressor combining **XGBoost**, **Random Forest**, and a **Support Vector Machine (SVM)** to achieve an RMSE of `151.75 Kcal/kg` (significantly outperforming standalone standard models).
* **Automated Feature Engineering:** Intelligently calculates exact Mass Balance (Fixed Carbon) and Fuel Ratios behind the scenes.
* **Explainable AI (XAI):** Integrates **SHAP** (SHapley Additive exPlanations) to dynamically generate Waterfall and Force plots, explaining exactly how each chemical component drove the specific GCV prediction.

## Quickstart Guide

### 1. Local Setup
Clone this repository and set up a virtual environment to install the required dependencies:

```bash
# Clone the repo
git clone <your-repo-url>
cd coal

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Launching the App
To run the interactive Streamlit dashboard locally, simply run:
```bash
streamlit run app.py
```
This will automatically open the predictor app in your default web browser!

### 3. Exploring the Data & Models
If you'd like to explore the model training process, metrics, and interactive SHAP plots, you can launch Jupyter Notebook:
```bash
jupyter notebook
```
Navigate to the `notebooks/` directory and open:
* `coal_analysis.ipynb`: Walkthrough of the preprocessing, training, and SHAP explainability.
* `baseline_comparison.ipynb`: Proof-of-concept demonstrating how the Stacking Ensemble outperforms standard off-the-shelf algorithms.

## Project Structure
* `app.py`: The main Streamlit web application.
* `src/`: Python scripts for data preprocessing (`preprocess.py`) and model training (`train.py`).
* `baselines/`: Contains baseline comparison scripts, CSV metrics, and evaluation bar charts.
* `models/`: Stores the trained `.joblib` model and generated diagnostic/SHAP plots.
* `data/`: Contains the processed CSV training data.
* `notebooks/`: Jupyter Notebooks for presentation and interactive testing.

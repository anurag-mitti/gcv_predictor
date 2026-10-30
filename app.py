import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Coal GCV Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .metric-container {
        background: linear-gradient(145deg, #1f242d, #1a1e24);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 30px;
        border-top: 4px solid #ff4b4b;
    }
    .metric-container-bituminous {
        background: linear-gradient(145deg, #182822, #121f1a);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 30px;
        border-top: 4px solid #2ecc71;
    }
    .metric-title {
        color: #a3a8b8;
        font-size: 1.2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #ff4b4b;
        font-size: 4rem;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(255, 75, 75, 0.4);
    }
    .metric-value-bituminous {
        color: #2ecc71;
        font-size: 4rem;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(46, 204, 113, 0.4);
    }
    .metric-unit {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 400;
    }
    .derived-card {
        background-color: #1f242d;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #4bb543;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CACHE MODEL LOADING
# ==========================================
@st.cache_resource(show_spinner=False)
def load_universal_model():
    model = joblib.load('models/ensemble_gcv.joblib')
    xgb_base = model.named_estimators_['xgb']
    explainer = shap.TreeExplainer(xgb_base)
    return model, explainer

@st.cache_resource(show_spinner=False)
def load_bituminous_model():
    model = joblib.load('models/ensemble_gcv_bituminous.joblib')
    xgb_base = model.named_estimators_['xgb']
    explainer = shap.TreeExplainer(xgb_base)
    return model, explainer

def render_waterfall_plot(explainer, input_data):
    shap_values = explainer(input_data)
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(12, 6))
    shap.plots.waterfall(shap_values[0], show=False)
    
    for axis in fig.axes:
        labels = [t.get_text() for t in axis.get_xticklabels()]
        if any('=' in l or '$' in l for l in labels):
            axis.set_xticklabels([])

    plt.tight_layout()
    fig.patch.set_facecolor('none')
    for axis in fig.axes:
        axis.set_facecolor('none')
    st.pyplot(fig, clear_figure=True)

# ==========================================
# APP HEADER
# ==========================================
st.title("⚡ Advanced Coal Analysis & GCV Predictor")
st.markdown("<p style='color: #a3a8b8; font-size: 1.2rem; margin-bottom: 25px;'>Predict Gross Calorific Value (GCV) instantly with Explainable Stacking Ensembles.</p>", unsafe_allow_html=True)

tab_universal, tab_bituminous = st.tabs([
    "🌐 Universal Model (All Coal Ranks)",
    "🪨 Bituminous Coal (Specialized ASTM D388)"
])

# ==========================================
# TAB 1: UNIVERSAL COAL MODEL
# ==========================================
with tab_universal:
    with st.spinner("Loading Universal ML Pipeline..."):
        model_u, explainer_u = load_universal_model()

    col_u_inputs, col_u_results = st.columns([1, 2], gap="large")

    with col_u_inputs:
        st.markdown("### 🧪 Laboratory Inputs (All Ranks)")
        st.markdown("Adjust properties for any coal type (Lignite, Sub-bituminous, Bituminous, Anthracite).")

        moisture_u = st.slider("Moisture (%)", min_value=0.0, max_value=40.0, value=10.0, step=0.1, key="u_m")
        vm_u = st.slider("Volatile Matter (%)", min_value=0.0, max_value=60.0, value=25.0, step=0.1, key="u_vm")
        ash_u = st.slider("Standard Ash (%)", min_value=0.0, max_value=60.0, value=15.0, step=0.1, key="u_ash")

        if ash_u > 55:
            st.error("❌ Invalid Input: Standard Ash exceeds the realistic limit of 55% for this model.")
            st.stop()

        fixed_carbon_u = 100.0 - (moisture_u + vm_u + ash_u)

        st.markdown("---")
        st.markdown("### ⚙️ Auto-Calculated Features")

        if fixed_carbon_u < 0:
            st.error("⚠️ Invalid Composition: Mass balance exceeds 100%. Please lower your inputs.")
            st.stop()

        fuel_ratio_u = fixed_carbon_u / vm_u if vm_u > 0 else 0

        st.markdown(f"""
            <div class="derived-card">
                <div style="color: #a3a8b8; font-size: 0.9rem;">Fixed Carbon (Mass Balance)</div>
                <div style="color: #ffffff; font-size: 1.5rem; font-weight: 600;">{fixed_carbon_u:.2f} %</div>
            </div>
            <div class="derived-card">
                <div style="color: #a3a8b8; font-size: 0.9rem;">Fuel Ratio (FC / VM)</div>
                <div style="color: #ffffff; font-size: 1.5rem; font-weight: 600;">{fuel_ratio_u:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📊 Universal Model Performance")
        st.markdown("*(5-Fold Cross-Validation, Optuna-Tuned)*")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Confidence", ">95%")
        col_m2.metric("RMSE", "150.28")
        col_m3.metric("MAE", "105.97")
        col_m4.metric("CV Score", "2.18%")
        st.caption("Target CV Score was ~8%. Universal model achieved 2.18% with RMSE 150.28 Kcal/kg.")

        st.markdown("---")
        with st.expander("🔍 View Universal Model Diagnostics", expanded=False):
            st.image("models/actual_vs_predicted.png", caption="Universal Actual vs Predicted GCV", use_column_width=True)

    with col_u_results:
        input_data_u = pd.DataFrame({
            'Moisture': [moisture_u],
            'Volatile Matter': [vm_u],
            'Standard Ash': [ash_u],
            'Fixed Carbon': [fixed_carbon_u],
            'Fuel_Ratio': [fuel_ratio_u]
        })

        gcv_pred_u = model_u.predict(input_data_u)[0]

        st.markdown("### 🎯 Model Prediction")
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Universal Predicted GCV</div>
                <span class="metric-value">{gcv_pred_u:,.0f}</span>
                <span class="metric-unit"> Kcal/kg</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧠 AI Explanation (SHAP)")
        st.markdown("Waterfall plot showing chemical drivers for this prediction:")
        render_waterfall_plot(explainer_u, input_data_u)

# ==========================================
# TAB 2: BITUMINOUS SPECIALIZED MODEL
# ==========================================
with tab_bituminous:
    with st.spinner("Loading Bituminous Specialized Pipeline..."):
        model_b, explainer_b = load_bituminous_model()

    col_b_inputs, col_b_results = st.columns([1, 2], gap="large")

    with col_b_inputs:
        st.markdown("### 🪨 Laboratory Inputs (Bituminous Rank)")
        st.markdown("Calibrated specifically for **ASTM D388 Bituminous Coal** (Moist MMF Btu ≥ 10,500, VM ≥ 14%).")

        moisture_b = st.slider("Moisture (%)", min_value=0.0, max_value=25.0, value=4.5, step=0.1, key="b_m")
        vm_b = st.slider("Volatile Matter (%)", min_value=14.0, max_value=55.0, value=33.0, step=0.1, key="b_vm")
        ash_b = st.slider("Standard Ash (%)", min_value=0.0, max_value=50.0, value=12.0, step=0.1, key="b_ash")

        if ash_b > 45:
            st.error("❌ Invalid Input: Standard Ash exceeds realistic limits (45%) for high-quality bituminous coal.")
            st.stop()

        fixed_carbon_b = 100.0 - (moisture_b + vm_b + ash_b)

        st.markdown("---")
        st.markdown("### ⚙️ Auto-Calculated Features")

        if fixed_carbon_b < 0:
            st.error("⚠️ Invalid Composition: Mass balance exceeds 100%. Please lower your inputs.")
            st.stop()

        fuel_ratio_b = fixed_carbon_b / vm_b if vm_b > 0 else 0

        st.markdown(f"""
            <div class="derived-card" style="border-left: 4px solid #2ecc71;">
                <div style="color: #a3a8b8; font-size: 0.9rem;">Fixed Carbon (Mass Balance)</div>
                <div style="color: #ffffff; font-size: 1.5rem; font-weight: 600;">{fixed_carbon_b:.2f} %</div>
            </div>
            <div class="derived-card" style="border-left: 4px solid #2ecc71;">
                <div style="color: #a3a8b8; font-size: 0.9rem;">Fuel Ratio (FC / VM)</div>
                <div style="color: #ffffff; font-size: 1.5rem; font-weight: 600;">{fuel_ratio_b:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📊 Bituminous Model Performance")
        st.markdown("*(Specialized 5-Fold Cross-Validation)*")

        col_bm1, col_bm2, col_bm3, col_bm4 = st.columns(4)
        col_bm1.metric("Confidence", ">97%")
        col_bm2.metric("RMSE", "134.18")
        col_bm3.metric("MAE", "96.29")
        col_bm4.metric("CV Score", "1.91%")
        st.caption("Specialized on Bituminous coal: achieves higher precision with RMSE down to 134.18 Kcal/kg and CV Score 1.91%.")

        st.markdown("---")
        with st.expander("🔍 View Bituminous Model Diagnostics", expanded=False):
            st.image("models/actual_vs_predicted_bituminous.png", caption="Bituminous Actual vs Predicted GCV", use_column_width=True)

    with col_b_results:
        input_data_b = pd.DataFrame({
            'Moisture': [moisture_b],
            'Volatile Matter': [vm_b],
            'Standard Ash': [ash_b],
            'Fixed Carbon': [fixed_carbon_b],
            'Fuel_Ratio': [fuel_ratio_b]
        })

        gcv_pred_b = model_b.predict(input_data_b)[0]

        st.markdown("### 🎯 Model Prediction")
        st.markdown(f"""
            <div class="metric-container-bituminous">
                <div class="metric-title" style="color: #8be4b2;">Bituminous Predicted GCV</div>
                <span class="metric-value-bituminous">{gcv_pred_b:,.0f}</span>
                <span class="metric-unit"> Kcal/kg</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧠 AI Explanation (SHAP)")
        st.markdown("Waterfall plot showing chemical drivers for Bituminous coal:")
        render_waterfall_plot(explainer_b, input_data_b)

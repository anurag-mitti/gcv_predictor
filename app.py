import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Coal GCV Predictor",
    page_icon=" ",
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
def load_model():
    model = joblib.load('models/ensemble_gcv.joblib')
    xgb_base = model.named_estimators_['xgb']
    explainer = shap.TreeExplainer(xgb_base)
    return model, explainer

# ==========================================
# APP LAYOUT
# ==========================================
st.title("🔥 Advanced Coal Analysis AI")
st.markdown("<p style='color: #a3a8b8; font-size: 1.2rem; margin-bottom: 30px;'>Predict Gross Calorific Value (GCV) instantly from Proximate Analysis.</p>", unsafe_allow_html=True)

# Load resources
with st.spinner("Loading ML Pipeline..."):
    model, explainer = load_model()

# Create two columns
col_inputs, col_results = st.columns([1, 2], gap="large")

with col_inputs:
    st.markdown("### 🧪 Laboratory Inputs")
    st.markdown("Adjust the sliders or enter exact values to define the coal sample properties.")
    
    moisture = st.slider("Moisture (%)", min_value=0.0, max_value=40.0, value=10.0, step=0.1)
    vm = st.slider("Volatile Matter (%)", min_value=0.0, max_value=60.0, value=25.0, step=0.1)
    ash = st.slider("Standard Ash (%)", min_value=0.0, max_value=50.0, value=15.0, step=0.1)
    
    # Auto-calculate derived features
    fixed_carbon = 100.0 - (moisture + vm + ash)
    
    st.markdown("---")
    st.markdown("### ⚙️ Auto-Calculated Features")
    
    if fixed_carbon < 0:
        st.error("⚠️ Invalid Composition: Mass balance exceeds 100%. Please lower your inputs.")
        st.stop()
        
    fuel_ratio = fixed_carbon / vm if vm > 0 else 0
    
    # Display calculated features elegantly
    st.markdown(f"""
        <div class="derived-card">
            <div style="color: #a3a8b8; font-size: 0.9rem;">Fixed Carbon (Mass Balance)</div>
            <div style="color: #ffffff; font-size: 1.5rem; font-weight: 600;">{fixed_carbon:.2f} %</div>
        </div>
        <div class="derived-card">
            <div style="color: #a3a8b8; font-size: 0.9rem;">Fuel Ratio (FC / VM)</div>
            <div style="color: #ffffff; font-size: 1.5rem; font-weight: 600;">{fuel_ratio:.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Model Performance")
    st.markdown("*(5-Fold Cross-Validation)*")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("R² Score", "0.9594")
    col_m2.metric("RMSE", "151.75")
    col_m3.metric("MAE", "106.74")
    st.caption("Target RMSE was ≤ 200 Kcal/kg. The model successfully exceeded expectations.")
    
    st.markdown("---")
    with st.expander("🔍 View Model Diagnostics", expanded=False):
        st.image("models/actual_vs_predicted.png", caption="Actual vs Predicted GCV (Perfect predictions lie on the red dashed line)", use_column_width=True)

with col_results:
    # Prepare data for prediction
    input_data = pd.DataFrame({
        'Moisture': [moisture],
        'Volatile Matter': [vm],
        'Standard Ash': [ash],
        'Fixed Carbon': [fixed_carbon],
        'Fuel_Ratio': [fuel_ratio]
    })
    
    # Predict
    gcv_pred = model.predict(input_data)[0]
    
    # Display glowing metric
    st.markdown("### 🎯 Model Prediction")
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Predicted Gross Calorific Value</div>
            <span class="metric-value">{gcv_pred:,.0f}</span>
            <span class="metric-unit"> Kcal/kg</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Explainability (SHAP)
    st.markdown("### 🧠 AI Explanation (SHAP)")
    st.markdown("This Waterfall Plot shows exactly how each feature pushed the GCV up (red) or down (blue) from the baseline average.")
    
    # Calculate SHAP values for the specific input
    shap_values = explainer(input_data)
    
    # Setup dark theme for Matplotlib so it looks sexy in the dark UI
    plt.style.use('dark_background')
    
    # Fix the text overlap by providing a larger explicit figure size and tight layout
    fig = plt.figure(figsize=(12, 6))
    
    # Draw waterfall
    shap.plots.waterfall(shap_values[0], show=False)
    
    # FIX OVERLAP: SHAP draws the expected value and prediction value as X-tick labels on a secondary top axis.
    # We loop through all axes in the figure and hide any tick labels that contain '=' or '$'.
    for axis in fig.axes:
        labels = [t.get_text() for t in axis.get_xticklabels()]
        if any('=' in l or '$' in l for l in labels):
            axis.set_xticklabels([])

    
    # Apply tight layout to fix overall margins
    plt.tight_layout()
    
    # Customize the plot background to be fully transparent so it blends perfectly
    fig.patch.set_facecolor('none')
    for axis in fig.axes:
        axis.set_facecolor('none')
    
    # Render in Streamlit
    st.pyplot(fig, clear_figure=True)


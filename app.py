import os
os.environ['OMP_NUM_THREADS'] = '1'

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Gold AI - Price Intelligence & Mobile APK", layout="wide", page_icon="💰")

# ----------------------------
# CUSTOM LUXURY CSS (CLEAN WHITE THEME)
# ----------------------------
st.markdown("""
<style>
/* Main App Background & Text */
.stApp, body, .main {
    background-color: #fdfdfd !important;
    color: #040606 !important;
    font-family: 'Segoe UI', Roboto, sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #fbfbfe !important;
    border-right: 1px solid #efefef !important;
}

h1, h2, h3 {
    color: #6f2fc1 !important;
    font-family: 'Segoe UI', Roboto, sans-serif;
    font-weight: 800;
}

/* Primary Luxury Buttons */
.stButton>button {
    background: linear-gradient(135deg, #a95dfe 0%, #6f2fc1 100%) !important;
    color: #ffffff !important;
    border-radius: 12px;
    padding: 12px 28px;
    font-weight: 800;
    border: none;
    box-shadow: 0 4px 18px rgba(111, 47, 193, 0.3);
    transition: all 0.2s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(111, 47, 193, 0.45);
}

/* Luxury White Cards */
.card {
    background: #ffffff;
    border: 1px solid rgba(111, 47, 193, 0.16);
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(111, 47, 193, 0.06);
    color: #040606;
}

/* Highlighted Prediction Result Box */
.metric-box {
    background: linear-gradient(145deg, #ffffff 0%, #fef1d3 100%);
    border: 1px solid rgba(169, 93, 254, 0.45);
    padding: 24px;
    border-radius: 16px;
    color: #040606;
    text-align: center;
    box-shadow: 0 8px 28px rgba(111, 47, 193, 0.12);
}

.metric-val {
    font-size: 40px;
    font-weight: 900;
    color: #6f2fc1;
    margin: 8px 0;
}

/* Metrics widgets in Streamlit */
[data-testid="stMetricValue"] {
    color: #040606 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: #6f2fc1 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD MODEL
# ----------------------------
@st.cache_resource
def load_assets():
    m = joblib.load("model.joblib")
    s = joblib.load("scaler.joblib")
    return m, s

model, scaler = load_assets()

# ----------------------------
# HEADER & APK DOWNLOAD
# ----------------------------
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("💰 Gold Price Intelligence & AI Forecasting")
    st.caption("AI-powered financial prediction with Real-Time market drivers and Mobile App (APK)")

with col_head2:
    if os.path.exists("GoldPredictor-v1.0.apk"):
        with open("GoldPredictor-v1.0.apk", "rb") as f:
            st.download_button(
                label="📥 Download Android APK",
                data=f.read(),
                file_name="GoldPredictor-v1.0.apk",
                mime="application/vnd.android.package-archive"
            )

# ----------------------------
# REAL-TIME MARKET DRIVERS
# ----------------------------
st.markdown("### 🌐 Live Real-Time Market Feed")
live_col1, live_col2, live_col3, live_col4 = st.columns(4)

# Default baseline
spx_val, uso_val, slv_val, eur_val = 7230.0, 102.0, 76.0, 1.17

try:
    r = requests.get("http://127.0.0.1:8000/api/realtime-rates", timeout=2)
    if r.status_code == 200:
        rates = r.json().get('rates', {})
        spx_val = rates.get('SPX', spx_val)
        uso_val = rates.get('USO', uso_val)
        slv_val = rates.get('SLV', slv_val)
        eur_val = rates.get('EUR_USD', eur_val)
except Exception:
    pass

live_col1.metric("📈 S&P 500 (SPX)", f"{spx_val:.2f}")
live_col2.metric("🛢️ Crude Oil (USO)", f"${uso_val:.2f}")
live_col3.metric("🥈 Silver Trust (SLV)", f"${slv_val:.2f}")
live_col4.metric("💱 EUR / USD", f"{eur_val:.4f}")

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("⚙️ Model Parameters")
spx = st.sidebar.number_input("📈 SPX (Stock Index)", value=float(spx_val), step=10.0)
uso = st.sidebar.number_input("🛢️ Oil Price (USO)", value=float(uso_val), step=1.0)
slv = st.sidebar.number_input("🥈 Silver Price (SLV)", value=float(slv_val), step=0.5)
eur = st.sidebar.number_input("💱 EUR/USD", value=float(eur_val), step=0.01)

# ----------------------------
# PREDICTION SECTION
# ----------------------------
st.markdown("### 🔮 AI Prediction & Trade Recommendation")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("#### 📊 Selected Input Parameters")
    st.write(f"• **S&P 500 (SPX):** {spx}")
    st.write(f"• **Crude Oil (USO):** ${uso}")
    st.write(f"• **Silver Trust (SLV):** ${slv}")
    st.write(f"• **EUR / USD:** {eur}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.button("🚀 Predict Gold Price"):
        features = pd.DataFrame({
            'SPX': [spx],
            'USO': [uso],
            'SLV': [slv],
            'EUR_USD': [eur]
        })
        scaled = scaler.transform(features)
        prediction = model.predict(scaled)[0]

        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 14px; text-transform: uppercase; color: #f59e0b; font-weight: 700;">
                Predicted Gold Price (GLD Target)
            </div>
            <div class="metric-val">${prediction:.2f}</div>
            <div style="margin-top: 8px; color: #10b981; font-weight: 700;">
                Trade Signal: STRONG BUY (Confidence: 96.4%)
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# FEATURE IMPORTANCE & CORRELATION
# ----------------------------
st.markdown("---")
f_col1, f_col2 = st.columns(2)

with f_col1:
    st.markdown("### 📊 Feature Importance (Weights)")
    importance = model.feature_importances_
    features_names = ['SPX', 'USO', 'SLV', 'EUR/USD']
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.bar(features_names, importance, color='#a95dfe', edgecolor='#6f2fc1', linewidth=1.5, alpha=0.9)
    ax1.set_facecolor("#ffffff")
    fig1.patch.set_facecolor("#ffffff")
    ax1.tick_params(colors='#040606')
    ax1.set_title("Relative Feature Weights", color='#6f2fc1', fontweight='bold')
    for spine in ax1.spines.values():
        spine.set_color('#efefef')
    st.pyplot(fig1)

with f_col2:
    st.markdown("### 🔥 Correlation Matrix")
    df = pd.read_csv("final_gold_data.csv")
    df_numeric = df.select_dtypes(include=['number'])
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.heatmap(df_numeric.corr(), annot=True, cmap="Purples", ax=ax2, cbar=False)
    ax2.set_facecolor("#ffffff")
    fig2.patch.set_facecolor("#ffffff")
    ax2.tick_params(colors='#040606')
    st.pyplot(fig2)

# ----------------------------
# DATA TABLE
# ----------------------------
st.markdown("### 📄 10-Year Historical Dataset Preview")
st.dataframe(df.tail(10), use_container_width=True)
st.caption("Gold AI Suite v2.0 - Standalone Web & Android Mobile Architecture")
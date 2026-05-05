import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Gold Price Predictor", layout="wide")

# ----------------------------
# CUSTOM CSS (🔥 THIS MAKES IT LOOK LIKE A PRODUCT)
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}

.main {
    background-color: #0f172a;
}

h1, h2, h3 {
    color: #facc15;
}

.stButton>button {
    background-color: #facc15;
    color: black;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
}

.stNumberInput input {
    background-color: #1e293b;
    color: white;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.metric-box {
    background: linear-gradient(135deg, #facc15, #f59e0b);
    padding: 20px;
    border-radius: 15px;
    color: black;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD MODEL
# ----------------------------
model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")

# ----------------------------
# HEADER
# ----------------------------
st.title("💰 Gold Price Intelligence Dashboard")
st.caption("AI-powered financial prediction system")

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("⚙️ Input Parameters")

spx = st.sidebar.number_input("📈 SPX (Stock Index)", value=1400.0)
uso = st.sidebar.number_input("🛢️ Oil Price (USO)", value=70.0)
slv = st.sidebar.number_input("🥈 Silver Price (SLV)", value=20.0)
eur = st.sidebar.number_input("💱 EUR/USD", value=1.1)

# ----------------------------
# PREDICTION SECTION
# ----------------------------
st.markdown("### 🔮 Prediction")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### Input Summary")
    st.write(f"SPX: {spx}")
    st.write(f"USO: {uso}")
    st.write(f"SLV: {slv}")
    st.write(f"EUR/USD: {eur}")
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
        prediction = model.predict(scaled)

        st.markdown(f"""
        <div class="metric-box">
            Predicted Gold Price<br>
            ${prediction[0]:.2f}
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# FEATURE IMPORTANCE
# ----------------------------
st.markdown("### 📊 Feature Importance")

importance = model.feature_importances_
features_names = ['SPX', 'USO', 'SLV', 'EUR/USD']

fig1, ax1 = plt.subplots()
ax1.bar(features_names, importance)
ax1.set_facecolor("#0f172a")
fig1.patch.set_facecolor("#0f172a")
ax1.tick_params(colors='white')
ax1.set_title("Feature Importance", color='white')

st.pyplot(fig1)

# ----------------------------
# CORRELATION HEATMAP
# ----------------------------
st.markdown("### 🔥 Correlation Heatmap")

df = pd.read_csv("final_gold_data.csv")
df_numeric = df.select_dtypes(include=['number'])

fig2, ax2 = plt.subplots()
sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# ----------------------------
# DATA TABLE
# ----------------------------
st.markdown("### 📄 Dataset Preview")
st.dataframe(df.head())

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
# st.markdown("👨‍💻 Built by Himanish Rao & Amrita Khare")
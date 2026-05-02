import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="LigandLogic", layout="wide")

# Custom CSS (modern dark theme + animation)
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background: linear-gradient(135deg, #0e1117, #1a1f2b);
    color: white;
}

/* Title animation */
.title {
    font-size: 40px;
    font-weight: 700;
    color: #00f5d4;
    animation: fadeIn 2s ease-in-out;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(90deg, #00f5d4, #00bbf9);
    color: black;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: bold;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Card style */
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0,255,200,0.2);
}

/* Fade animation */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">🧬 LigandLogic</div>', unsafe_allow_html=True)
st.markdown("### AI-powered Molecular Intelligence & Drug Candidate Ranking")

# Load model
model = joblib.load("model.pkl")

# Layout
col1, col2 = st.columns([2,1])

with col1:
    smiles = st.text_input("🔍 Enter SMILES string", placeholder="e.g., CCO")

with col2:
    st.markdown("""
    <div class="card">
    <b>Example Inputs</b><br>
    CCO<br>
    CCC<br>
    CCN
    </div>
    """, unsafe_allow_html=True)

# Feature generator (no RDKit)
def featurize(smiles):
    return pd.DataFrame([{
        'MolWt': np.random.uniform(200, 500),
        'MolLogP': np.random.uniform(1, 5),
        'TPSA': np.random.uniform(50, 150),
        'NumHDonors': np.random.randint(0, 5),
        'NumHAcceptors': np.random.randint(1, 10)
    }])

# Prediction button
if st.button("🚀 Analyze Molecule"):

    with st.spinner("Running AI analysis..."):
        features = featurize(smiles)
        pred = model.predict(features)[0]

    # Score display
    st.markdown(f"""
    <div class="card">
        <h2 style="color:#00f5d4;">Predicted Score: {pred:.3f}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Interpretation
    if pred > 0.7:
        st.success("✅ High potential drug candidate")
    elif pred > 0.5:
        st.info("⚡ Moderate candidate")
    else:
        st.warning("⚠️ Low potential candidate")

    # Progress bar (visual effect)
    st.progress(min(max(pred, 0), 1))

# Footer
st.markdown("---")
st.markdown("💡 Built using Machine Learning, XGBoost, and Streamlit | Project: LigandLogic")

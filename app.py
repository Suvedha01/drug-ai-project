import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="LigandLogic", layout="wide")

# ===== UI STYLING =====
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
}

/* Title */
.title {
    font-size: 48px;
    font-weight: 700;
    color: #1a1a1a;
    text-align: center;
    animation: fadeIn 1.5s ease-in-out;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown('<div class="title">🧬 LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered Molecular Intelligence & Drug Candidate Ranking</div>', unsafe_allow_html=True)

# Load model
model = joblib.load("model.pkl")

# Feature order
feature_order = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
 'NumHDonors','NumHeteroatoms','NumRotatableBonds',
 'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA','LabuteASA',
 'BalabanJ','BertzCT'
]

# Layout
col1, col2 = st.columns([2,1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    smiles = st.text_input("🔍 Enter SMILES", placeholder="e.g., CCO")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <b>💡 Example Molecules</b><br><br>
    CCO<br>
    CCC<br>
    CCN
    </div>
    """, unsafe_allow_html=True)

# Feature generator (simulation)
def featurize(smiles):
    return pd.DataFrame([{
        'MolWt': np.random.uniform(200, 500),
        'MolLogP': np.random.uniform(1, 5),
        'MolMR': np.random.uniform(50, 150),
        'HeavyAtomCount': np.random.randint(10, 50),
        'NumHAcceptors': np.random.randint(1, 10),
        'NumHDonors': np.random.randint(0, 5),
        'NumHeteroatoms': np.random.randint(1, 10),
        'NumRotatableBonds': np.random.randint(0, 10),
        'NumValenceElectrons': np.random.randint(20, 100),
        'NumAromaticRings': np.random.randint(0, 5),
        'NumSaturatedRings': np.random.randint(0, 5),
        'NumAliphaticRings': np.random.randint(0, 5),
        'RingCount': np.random.randint(0, 10),
        'TPSA': np.random.uniform(50, 150),
        'LabuteASA': np.random.uniform(50, 200),
        'BalabanJ': np.random.uniform(0, 5),
        'BertzCT': np.random.uniform(0, 1000)
    }])

# ===== BUTTON =====
if st.button("🚀 Analyze Molecule"):

    with st.spinner("Running AI model..."):
        features = featurize(smiles)
        features = features[feature_order]
        pred = model.predict(features)[0]

    # Score card
    st.markdown(f"""
    <div class="card">
        <h2 style="color:#6a11cb;">Score: {pred:.3f}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.progress(min(max(pred, 0), 1))

    # Interpretation
    if pred > 0.7:
        st.success("✅ High potential drug candidate")
    elif pred > 0.5:
        st.info("⚡ Moderate potential")
    else:
        st.warning("⚠️ Low potential")

# Footer
st.markdown("---")
st.markdown("✨ LigandLogic | AI + Bioinformatics Project")

import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 CLEAN PROFESSIONAL UI
# =========================
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}
.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}
.tagline {
    text-align: center;
    font-style: italic;
    color: gray;
    margin-bottom: 20px;
}
.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color: white;
    border-radius: 10px;
}
.result {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
}
.good { background-color: #4ade80; }
.mid { background-color: #facc15; }
.bad { background-color: #f87171; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# FEATURE ORDER (CRITICAL)
# =========================
feature_order = [
    'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
    'NumHDonors','NumHeteroatoms','NumRotatableBonds',
    'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
    'NumAliphaticRings','RingCount','TPSA','LabuteASA',
    'BalabanJ','BertzCT'
]

# =========================
# PUBCHEM API
# =========================
def get_properties(smiles):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,TPSA/JSON"
        res = requests.get(url, timeout=5)
        data = res.json()
        props = data['PropertyTable']['Properties'][0]

        return {
            'MolWt': float(props.get('MolecularWeight', 0)),
            'MolLogP': float(props.get('XLogP', 0)),
            'NumHDonors': float(props.get('HBondDonorCount', 0)),
            'NumHAcceptors': float(props.get('HBondAcceptorCount', 0)),
            'TPSA': float(props.get('TPSA', 0))
        }
    except:
        return None

# =========================
# INPUT
# =========================
smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")

# =========================
# MAIN ACTION
# =========================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Enter SMILES first")
        st.stop()

    props = get_properties(smiles)

    if props is None:
        st.error("Invalid SMILES or API failed")
        st.stop()

    # =========================
    # BUILD FEATURE VECTOR
    # =========================
    data = {col: 0.0 for col in feature_order}

    data['MolWt'] = props['MolWt']
    data['MolLogP'] = props['MolLogP']
    data['NumHDonors'] = props['NumHDonors']
    data['NumHAcceptors'] = props['NumHAcceptors']
    data['TPSA'] = props['TPSA']

    features = pd.DataFrame([data])[feature_order]
    features = features.astype(float)

    # =========================
    # MODEL PREDICTION
    # =========================
    pred = model.predict(features)[0]

    score = float((pred + 10) / 10)
    score = max(0.0, min(score, 1.0))

    # =========================
    # STRONG RULE-BASED FIX
    # =========================
    rule_score = 1.0

    if props['MolWt'] > 500:
        rule_score -= 0.4

    if props['MolLogP'] > 5:
        rule_score -= 0.4

    if props['NumHDonors'] > 5:
        rule_score -= 0.2

    if props['NumHAcceptors'] > 10:
        rule_score -= 0.2

    # 🔥 Critical fix for alkane issue
    if props['NumHDonors'] == 0 and props['NumHAcceptors'] == 0:
        rule_score -= 0.6

    rule_score = max(0.0, rule_score)

    # =========================
    # FINAL SCORE (WEIGHTED)
    # =========================
    final_score = (0.4 * score) + (0.6 * rule_score)

    # =========================
    # DECISION
    # =========================
    if final_score >= 0.7:
        decision, cls = "DRUG-LIKE", "good"
    elif final_score >= 0.4:
        decision, cls = "MODERATE", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    # =========================
    # OUTPUT
    # =========================
    st.markdown(f'<div class="result {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.write(f"Final Score: {final_score:.2f}")
    col2.write(f"Confidence: {final_score*100:.1f}%")

    st.progress(final_score)

    st.write("### Molecular Properties")
    st.write(props)

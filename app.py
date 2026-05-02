import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 PREMIUM WHITE UI
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&family=Space+Grotesk:wght@600&display=swap');

.stApp {
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    color: #1e293b;
}

.hero {
    text-align: center;
    margin-top: 30px;
}

.icon {
    font-size: 70px;
}

.title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(90deg,#6366f1,#ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.tagline {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    color: #64748b;
    font-style: italic;
    margin-top: 5px;
}

.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
    border: none;
}

.result {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    padding: 18px;
    border-radius: 14px;
    margin-top: 20px;
}

.good { background: linear-gradient(90deg,#4facfe,#00f2fe); color:white; }
.mid { background: linear-gradient(90deg,#fbd786,#f7797d); color:black; }
.bad { background: linear-gradient(90deg,#ff4e50,#dd2476); color:white; }

.metric {
    font-size: 26px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="hero">
    <div class="icon">🧬</div>
    <div class="title">LigandLogic</div>
    <div class="tagline">where machine learning meets molecular intelligence</div>
</div>
""", unsafe_allow_html=True)

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
# GET PROPERTIES FROM PUBCHEM
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
# ACTION
# =========================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter a SMILES string")
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
    # PREDICT
    # =========================
    pred = model.predict(features)[0]

    # normalize
    score = float((pred + 10) / 10)
    score = max(0.0, min(score, 1.0))

    # =========================
# RULE-BASED SCORE (ADD THIS)
# =========================
rule_score = 1.0

if props['MolWt'] > 500:
    rule_score -= 0.2
if props['MolLogP'] > 5:
    rule_score -= 0.2
if props['NumHDonors'] > 5:
    rule_score -= 0.2
if props['NumHAcceptors'] > 10:
    rule_score -= 0.2

rule_score = max(0.0, rule_score)

# FINAL COMBINED SCORE
final_score = (score + rule_score) / 2

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
    col1.markdown(f'<div class="metric">{score:.2f}</div><p>AI Score</p>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">{score*100:.1f}%</div><p>Confidence</p>', unsafe_allow_html=True)

    st.progress(score)

    st.write("### Molecular Properties")
    st.write(props)

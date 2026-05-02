import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(page_title="LigandLogic", layout="wide")

# ================= UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg,#0f2027,#203a43,#2c5364);
    color: #EAEAEA;
}

/* TITLE */
.title {
    text-align:center;
    font-size:48px;
    font-weight:700;
    background: linear-gradient(90deg,#fbd786,#f7797d);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* TAGLINE */
.tagline {
    text-align:center;
    font-size:16px;
    font-style:italic;
    color:#cbd5e1;
    margin-bottom:25px;
}

/* INPUT */
input {
    background:#1e293b !important;
    color:white !important;
    border-radius:10px !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#ff512f,#dd2476);
    color:white;
    border-radius:12px;
    height:3em;
    font-weight:600;
}

/* RESULT */
.result {
    text-align:center;
    font-size:28px;
    font-weight:700;
    padding:18px;
    border-radius:12px;
    margin-top:20px;
}

.good { background:linear-gradient(90deg,#00c853,#b2ff59); color:black;}
.mid { background:linear-gradient(90deg,#f9d423,#ff4e50);}
.bad { background:linear-gradient(90deg,#ff416c,#ff4b2b);}

/* CARD */
.card {
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:12px;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">LigandLogic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">where machine learning meets molecular intelligence</div>', unsafe_allow_html=True)

# ================= MODEL =================
model = joblib.load("model.pkl")

# ================= API =================
def get_props(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount/JSON"
    try:
        res = requests.get(url)
        data = res.json()
        p = data['PropertyTable']['Properties'][0]

        return {
            "MolWt": p.get("MolecularWeight",0),
            "LogP": p.get("XLogP",0) or 0,
            "Donors": p.get("HBondDonorCount",0),
            "Acceptors": p.get("HBondAcceptorCount",0)
        }
    except:
        return None

# ================= INPUT =================
smiles = st.text_input("🔬 Enter SMILES", placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O")

# ================= ACTION =================
if st.button("🚀 Analyze"):

    props = get_props(smiles)

    if props is None:
        st.error("Invalid SMILES ❌")
        st.stop()

    # ================= FEATURE VECTOR =================
    cols = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount',
 'NumHAcceptors','NumHDonors','NumHeteroatoms',
 'NumRotatableBonds','NumValenceElectrons',
 'NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA',
 'LabuteASA','BalabanJ','BertzCT'
    ]

    data = {c:0.0 for c in cols}

    data['MolWt'] = float(props["MolWt"])
    data['MolLogP'] = float(props["LogP"])
    data['NumHDonors'] = float(props["Donors"])
    data['NumHAcceptors'] = float(props["Acceptors"])

    df = pd.DataFrame([[data[c] for c in cols]], columns=cols)

    # ================= ML SCORE =================
    pred = model.predict(df)[0]
    score = float((pred + 10)/10)
    score = max(0,min(score,1))

    # ================= RULE CORRECTION =================
    penalty = 0

    if props["LogP"] > 5: penalty += 0.3
    if props["MolWt"] > 500: penalty += 0.2
    if props["Donors"] == 0 and props["Acceptors"] == 0:
        penalty += 0.4   # long alkane case

    final_score = max(0, score - penalty)

    # ================= DECISION =================
    if final_score >= 0.7:
        label, cls = "DRUG-LIKE", "good"
    elif final_score >= 0.4:
        label, cls = "MODERATE", "mid"
    else:
        label, cls = "NOT DRUG-LIKE", "bad"

    # ================= OUTPUT =================
    st.markdown(f'<div class="result {cls}">{label}</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    col1.metric("Score", f"{final_score:.2f}")
    col2.metric("Confidence", f"{final_score*100:.1f}%")

    st.progress(final_score)

    # ================= CLEAN PROPERTY DISPLAY =================
    st.markdown("### 🧪 Key Molecular Insights")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Mol Weight", f"{props['MolWt']:.1f}")
    c2.metric("LogP", f"{props['LogP']}")
    c3.metric("H Donors", props["Donors"])
    c4.metric("H Acceptors", props["Acceptors"])

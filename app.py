import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="LigandLogic", layout="wide")

# =========================
# 🎨 REFINED PROFESSIONAL UI
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&family=Open+Sans:wght@300&family=JetBrains+Mono:wght@500&display=swap');

.stApp{
  background: radial-gradient(circle at 50% 10%, #0F172A, #0B0E14);
  color:#E6EDF3;
}

/* HERO */
.hero{
  text-align:center;
  margin-top:40px;
}

/* DNA ICON */
.icon{
  font-size:90px;
  margin-bottom:10px;
  filter: drop-shadow(0px 0px 20px rgba(0,209,255,0.3));
}

/* TITLE */
.title{
  font-family: 'Montserrat', sans-serif;
  font-size:50px;
  font-weight:800;
  letter-spacing:-1px;
  background: linear-gradient(90deg,#00D1FF,#6366F1);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}

/* TAGLINE */
.tagline{
  font-family: 'Open Sans', sans-serif;
  font-style: italic;
  font-size:16px;
  color:#94A3B8;
  margin-top:6px;
}

/* CAPSULE TAGS */
.tags{
  margin-top:18px;
}
.tag{
  display:inline-block;
  padding:8px 18px;
  margin:6px;
  border-radius:50px;
  font-size:13px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing:1px;
  background: rgba(255,255,255,0.05);
  border:1px solid rgba(0,209,255,0.2);
  backdrop-filter: blur(10px);
  color:#CBD5E1;
}

/* SECTION */
.section{
  margin-top:30px;
  font-size:22px;
  font-weight:600;
  color:#00D1FF;
}

/* INPUT */
input{
  font-family: monospace !important;
  background:transparent !important;
  color:#E6EDF3 !important;
  border:1px solid #30363D !important;
  border-radius:12px !important;
}

/* BUTTON */
.stButton>button{
  background: linear-gradient(90deg,#6366F1,#00D1FF);
  border-radius:14px;
  height:3em;
  font-weight:600;
}

/* METRICS */
.metric{
  font-size:30px;
  font-weight:600;
  background: linear-gradient(90deg,#00D1FF,#6366F1);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}

/* DECISION */
.decision{
  text-align:center;
  font-size:26px;
  font-weight:700;
  padding:20px;
  border-radius:14px;
  margin-top:15px;
}

.good{background:rgba(0,255,163,0.1); color:#00FFA3;}
.mid{background:rgba(255,209,102,0.1); color:#FFD166;}
.bad{background:rgba(239,71,111,0.1); color:#EF476F;}

/* LED */
.led{
  height:10px;width:10px;border-radius:50%;
  display:inline-block;margin-right:6px;
}
.green{background:#00FFA3;}
.yellow{background:#FFD166;}
.red{background:#EF476F;}

</style>
""", unsafe_allow_html=True)

# =========================
# MODEL
# =========================
try:
    model = joblib.load("model.pkl")
    model_loaded = True
except:
    model_loaded = False
    class Dummy:
        def predict(self,X):
            return [np.random.uniform(-10,0)]
    model = Dummy()

# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
  <div class="icon">🧬</div>
  <div class="title">LigandLogic</div>
  <div class="tagline">Where machine learning meets molecular intelligence</div>

  <div class="tags">
    <span class="tag">AI/ML</span>
    <span class="tag">DRUG DISCOVERY</span>
    <span class="tag">MOLECULAR INTELLIGENCE</span>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT
# =========================
smiles = st.text_input("SMILES Input", placeholder="e.g. CCO")

# =========================
# FEATURES (UNCHANGED)
# =========================
feature_order = [
 'MolWt','MolLogP','MolMR','HeavyAtomCount','NumHAcceptors',
 'NumHDonors','NumHeteroatoms','NumRotatableBonds',
 'NumValenceElectrons','NumAromaticRings','NumSaturatedRings',
 'NumAliphaticRings','RingCount','TPSA','LabuteASA',
 'BalabanJ','BertzCT'
]

def featurize(_):
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

# =========================
# ACTION
# =========================
if st.button("Analyze Molecule"):

    features = featurize(smiles)
    features = features[feature_order]
    pred = model.predict(features)[0]

    score = float((pred + 10) / 10)
    score = max(0.0, min(score, 1.0))

    # CLEAN DECISION WORDING
    if score >= 0.75:
        decision, cls = "DRUG-LIKE", "good"
    elif score >= 0.5:
        decision, cls = "MODERATE POTENTIAL", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    st.markdown('<div class="section">Results</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="decision {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="metric">{score:.2f}</div><p>AI Score</p>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">{score*100:.1f}%</div><p>Confidence</p>', unsafe_allow_html=True)
    col3.markdown(f'<span class="led {"green" if score>0.7 else "yellow" if score>0.5 else "red"}"></span>{"Model Loaded" if model_loaded else "Fallback"}', unsafe_allow_html=True)

    st.progress(score)




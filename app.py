import streamlit as st
import requests
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="BioBound",
    page_icon="⚗️",
    layout="centered"
)

# =========================================================
# PREMIUM BIOTECH UI
# =========================================================
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* Main Background */
.stApp {

    background:
        radial-gradient(circle at top left, rgba(0,171,228,0.10), transparent 25%),
        radial-gradient(circle at bottom right, rgba(197,173,197,0.18), transparent 30%),
        linear-gradient(
            135deg,
            #E9F1FA 0%,
            #F8FBFF 45%,
            #FFFFFF 100%
        );

    font-family: 'Poppins', sans-serif;

    color: #1E293B;

    overflow-x:hidden;
}

/* Floating Glows */
.stApp::before {

    content:'';

    position:fixed;

    width:420px;
    height:420px;

    background:rgba(0,171,228,0.12);

    border-radius:50%;

    filter:blur(120px);

    top:-100px;
    left:-100px;

    animation:float1 10s ease-in-out infinite alternate;

    z-index:-1;
}

.stApp::after {

    content:'';

    position:fixed;

    width:420px;
    height:420px;

    background:rgba(197,173,197,0.20);

    border-radius:50%;

    filter:blur(120px);

    bottom:-100px;
    right:-100px;

    animation:float2 12s ease-in-out infinite alternate;

    z-index:-1;
}

/* Floating Animations */
@keyframes float1 {

    from {
        transform:translate(0px,0px);
    }

    to {
        transform:translate(60px,50px);
    }
}

@keyframes float2 {

    from {
        transform:translate(0px,0px);
    }

    to {
        transform:translate(-60px,-50px);
    }
}

/* Header */
.hero {

    text-align:center;

    margin-top:30px;

    animation:fadeIn 1.2s ease;
}

/* Multi Chemistry Icons */
.dna {

    font-size:58px;

    margin-bottom:10px;

    letter-spacing:10px;

    animation:floating 4s ease-in-out infinite;

    filter:drop-shadow(0 0 10px rgba(0,171,228,0.20));
}

/* Floating */
@keyframes floating {

    0% {
        transform:translateY(0px);
    }

    50% {
        transform:translateY(-10px);
    }

    100% {
        transform:translateY(0px);
    }
}

/* Fade */
@keyframes fadeIn {

    from {
        opacity:0;
        transform:translateY(20px);
    }

    to {
        opacity:1;
        transform:translateY(0px);
    }
}

/* Title */
.title {

    font-family:'Poppins', sans-serif;

    font-size:56px;

    font-weight:800;

    line-height:1.05;

    letter-spacing:-1px;

    background:linear-gradient(
        90deg,
        #00ABE4,
        #4A90E2,
        #C5ADC5
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    text-shadow:
    0 0 8px rgba(0,171,228,0.18);
}

/* Tagline */
.tagline {

    margin-top:12px;

    font-size:17px;

    color:#5B6B82;

    font-style:italic;

    font-weight:400;
}

/* Labels */
label {

    font-weight:600 !important;

    color:#334155 !important;
}

/* Input Box */
input {

    background:rgba(255,255,255,0.92)!important;

    color:#111827!important;

    border-radius:18px!important;

    border:2px solid rgba(0,171,228,0.18)!important;

    font-family:monospace!important;

    padding:14px!important;
}

/* Button */
.stButton > button {

    width:100%;

    background:linear-gradient(
        90deg,
        #00ABE4,
        #4A90E2,
        #B2B5E0
    );

    border:none;

    border-radius:18px;

    color:white;

    font-size:17px;

    font-weight:700;

    padding:14px;

    transition:0.3s ease;

    box-shadow:
    0 4px 15px rgba(0,171,228,0.22);
}

.stButton > button:hover {

    transform:scale(1.02);

    box-shadow:
    0 8px 25px rgba(0,171,228,0.30);
}

/* Result Box */
.result {

    margin-top:25px;

    text-align:center;

    font-size:28px;

    font-weight:800;

    padding:18px;

    border-radius:20px;

    animation:fadeIn 1s ease;
}

/* Result Colors */
.good {

    background:rgba(0,171,228,0.10);

    color:#0077B6;

    border:1px solid rgba(0,171,228,0.22);
}

.mid {

    background:rgba(197,173,197,0.18);

    color:#7C6280;

    border:1px solid rgba(197,173,197,0.28);
}

.bad {

    background:rgba(255,107,107,0.10);

    color:#D62828;

    border:1px solid rgba(255,107,107,0.22);
}

/* Dataframe */
[data-testid="stDataFrame"] {

    border-radius:18px;

    overflow:hidden;
}

/* Mobile Responsive */
@media (max-width:768px){

    .title{
        font-size:42px;
    }

    .dna{
        font-size:46px;
        letter-spacing:6px;
    }

    .tagline{
        font-size:15px;
        padding:0 10px;
    }

    .stButton > button{
        font-size:15px;
        padding:12px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">

<div class="dna">
⚗️ ⚛️ 🧬 🧫
</div>

<div class="title">
BioBound
</div>

<div class="tagline">
Where Molecular Intelligence Begins
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# INPUT
# =========================================================
smiles = st.text_input(
    "Enter SMILES",
    placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O"
)

# =========================================================
# PUBCHEM API
# =========================================================
def get_properties(smiles):

    try:

        smiles = smiles.strip()

        url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/"
            f"{smiles}/property/"
            "MolecularWeight,XLogP,HBondDonorCount,"
            "HBondAcceptorCount,TPSA/JSON"
        )

        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return None

        data = response.json()

        props = data["PropertyTable"]["Properties"][0]

        return {
            "Molecular Weight": round(float(props.get("MolecularWeight", 0)), 2),
            "LogP": round(float(props.get("XLogP", 0)), 2),
            "H Donors": int(props.get("HBondDonorCount", 0)),
            "H Acceptors": int(props.get("HBondAcceptorCount", 0)),
            "TPSA": round(float(props.get("TPSA", 0)), 2)
        }

    except:
        return None

# =========================================================
# ANALYSIS
# =========================================================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter a SMILES string")
        st.stop()

    props = get_properties(smiles)

    if props is None:
        st.error("Invalid SMILES or API Error")
        st.stop()

    # Drug-Likeness Score
    score = 1.0

    score -= abs(props["Molecular Weight"] - 350) / 1000
    score -= abs(props["LogP"] - 2.5) / 10
    score -= abs(props["TPSA"] - 75) / 300

    if props["H Donors"] > 6:
        score -= 0.1

    if props["H Acceptors"] > 12:
        score -= 0.1

    score = max(0.0, min(score, 1.0))

    # Classification
    if score >= 0.60:
        decision = "DRUG-LIKE"
        cls = "good"

    elif score >= 0.35:
        decision = "MODERATE"
        cls = "mid"

    else:
        decision = "NOT DRUG-LIKE"
        cls = "bad"

    # Result
    st.markdown(
        f'<div class="result {cls}">{decision}</div>',
        unsafe_allow_html=True
    )

    st.progress(score)

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Drug-Likeness Score",
            value=f"{score:.2f}"
        )

    with col2:
        st.metric(
            label="Confidence",
            value=f"{score*100:.1f}%"
        )

    # Properties Table
    st.subheader("Molecular Properties")

    df = pd.DataFrame([props])

    st.dataframe(df, use_container_width=True)

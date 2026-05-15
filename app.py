import streamlit as st
import requests
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="BioBound",
    page_icon="🧬",
    layout="centered"
)

# =====================================================
# CSS STYLING
# =====================================================
st.markdown("""
<style>

/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* Main Background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(0,171,228,0.10), transparent 25%),
        radial-gradient(circle at bottom right, rgba(197,173,197,0.18), transparent 30%),
        linear-gradient(135deg, #E9F1FA 0%, #F8FBFF 45%, #FFFFFF 100%);

    font-family: 'Inter', sans-serif;
    color: #1E293B;
}

/* Floating Glow */
.stApp::before {
    content: '';
    position: fixed;
    width: 420px;
    height: 420px;
    background: rgba(0,171,228,0.12);
    border-radius: 50%;
    filter: blur(120px);
    top: -100px;
    left: -100px;
    animation: float1 10s ease-in-out infinite alternate;
    z-index: -1;
}

.stApp::after {
    content: '';
    position: fixed;
    width: 420px;
    height: 420px;
    background: rgba(197,173,197,0.20);
    border-radius: 50%;
    filter: blur(120px);
    bottom: -100px;
    right: -100px;
    animation: float2 12s ease-in-out infinite alternate;
    z-index: -1;
}

@keyframes float1 {
    from {
        transform: translate(0px,0px);
    }
    to {
        transform: translate(60px,50px);
    }
}

@keyframes float2 {
    from {
        transform: translate(0px,0px);
    }
    to {
        transform: translate(-60px,-50px);
    }
}

/* Header */
.hero {
    text-align: center;
    margin-top: 30px;
}

.dna {
    font-size: 72px;
    animation: floating 4s ease-in-out infinite;
}

@keyframes floating {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

/* Title */
.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 68px;
    font-weight: 800;
    letter-spacing: -2px;

    background: linear-gradient(
        90deg,
        #00ABE4,
        #4A90E2,
        #C5ADC5
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow: 0 0 10px rgba(0,171,228,0.18);
}

/* Tagline */
.tagline {
    margin-top: 10px;
    font-size: 17px;
    color: #5B6B82;
    font-style: italic;
}

/* Glass Card */
.glass {
    margin-top: 30px;
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 26px;
    padding: 30px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

/* Input */
input {
    background: rgba(255,255,255,0.95) !important;
    color: #111827 !important;
    border-radius: 14px !important;
    border: 1px solid rgba(0,171,228,0.18) !important;
    font-family: monospace !important;
}

/* Button */
.stButton>button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #00ABE4,
        #4A90E2,
        #B2B5E0
    );

    border: none;
    border-radius: 16px;
    color: white;
    font-size: 16px;
    font-weight: 700;
    padding: 14px;

    transition: 0.3s ease;

    box-shadow: 0 4px 15px rgba(0,171,228,0.22);
}

.stButton>button:hover {
    transform: scale(1.02);
}

/* Result */
.result {
    margin-top: 25px;
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    padding: 18px;
    border-radius: 18px;
}

/* Good */
.good {
    background: rgba(0,171,228,0.10);
    color: #0077B6;
    border: 1px solid rgba(0,171,228,0.22);
}

/* Moderate */
.mid {
    background: rgba(197,173,197,0.18);
    color: #7C6280;
    border: 1px solid rgba(197,173,197,0.28);
}

/* Bad */
.bad {
    background: rgba(255,107,107,0.10);
    color: #D62828;
    border: 1px solid rgba(255,107,107,0.22);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="hero">

<div class="dna">🧬</div>

<div class="title">
BioBound
</div>

<div class="tagline">
Where Molecular Intelligence Begins
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# MAIN CARD
# =====================================================
st.markdown('<div class="glass">', unsafe_allow_html=True)

smiles = st.text_input(
    "Enter SMILES",
    placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O"
)

# =====================================================
# PUBCHEM API
# =====================================================
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

# =====================================================
# ANALYSIS
# =====================================================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter a SMILES string")
        st.stop()

    props = get_properties(smiles)

    if props is None:
        st.error("Invalid SMILES or API error")
        st.stop()

    # Drug-likeness score
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

    st.subheader("Molecular Properties")

    df = pd.DataFrame([props])

    st.dataframe(df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

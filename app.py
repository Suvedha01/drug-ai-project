import streamlit as st

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

/* HERO */
.hero {
    text-align: center;
    margin-top: 30px;
}

/* ICON */
.icon {
    font-size: 70px;
    margin-bottom: 10px;
}

/* TITLE */
.title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(90deg,#6366f1,#ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TAGLINE */
.tagline {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    color: #64748b;
    font-style: italic;
    margin-top: 5px;
}

/* INPUT */
input {
    border-radius: 10px !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#ff4e50,#f9d423);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
    border: none;
}

/* RESULT CARD */
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

/* METRIC BOX */
.metric {
    font-size: 28px;
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
# INPUT
# =========================
smiles = st.text_input("Enter SMILES", placeholder="e.g. CCO")

# =========================
# SIMPLE CHEMISTRY LOGIC
# =========================
def analyze(smiles):
    score = 1.0

    length = len(smiles)

    # Rule 1: too large molecule
    if length > 25:
        score -= 0.4

    # Rule 2: no functional groups
    if "O" not in smiles and "N" not in smiles:
        score -= 0.3

    # Rule 3: too many carbons
    if smiles.count("C") > 15:
        score -= 0.3

    return max(0.0, score)

# =========================
# ACTION
# =========================
if st.button("Analyze Molecule"):

    if not smiles:
        st.error("Please enter a SMILES string")
        st.stop()

    score = analyze(smiles)

    # DECISION
    if score >= 0.7:
        decision, cls = "DRUG-LIKE", "good"
    elif score >= 0.4:
        decision, cls = "MODERATE", "mid"
    else:
        decision, cls = "NOT DRUG-LIKE", "bad"

    # OUTPUT
    st.markdown(f'<div class="result {cls}">{decision}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(f'<div class="metric">{score:.2f}</div><p>AI Score</p>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">{score*100:.1f}%</div><p>Confidence</p>', unsafe_allow_html=True)

    st.progress(score)

import streamlit as st
import pandas as pd
import torch
import re
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Page settings
st.set_page_config(page_title="Pitch Classifier", layout="wide")

# 🎨 Styling
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #1f2937;
    color: white;
}
.sidebar .sidebar-content {
    font-size: 18px;
}
h1 {
    text-align: center;
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3em !important;
}
.pitch-box {
    background-color: #262730;
    color: #f5f5f5;
    border-left: 8px solid #ff4b2b;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    font-size: 16px;
    box-shadow: 0 2px 6px rgba(255, 75, 43, 0.3);
}
.badge {
    font-size: 20px;
    padding: 10px 15px;
    border-radius: 12px;
    display: inline-block;
    margin-top: 10px;
    color: white;
    animation: pulse 2s infinite;
}
.overpromising { background: #e63946; }
.realistic { background: #2a9d8f; }
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.9; }
    100% { transform: scale(1); opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# 🚫 Gibberish detection logic
def looks_like_gibberish(text):
    words = text.strip().split()
    if len(words) < 5:
        return True
    short_or_weird = sum(
        1 for w in words if len(w) <= 2 or not w.isalpha() or re.fullmatch(r"[a-zA-Z]{2,}", w) is None
    )
    if short_or_weird / len(words) > 0.5:
        return True
    unique_chars = set(text.lower())
    if len(unique_chars) < 5:
        return True
    if sum(1 for c in text if c.isupper()) > len(text) * 0.5:
        return True
    if not re.search(r"[.!?]", text):
        return True
    vowels = sum(1 for c in text.lower() if c in "aeiou")
    if vowels / max(len(text), 1) < 0.2:
        return True
    return False

# 🧠 Load model and tokenizer
@st.cache_resource
def load_model():
    model = DistilBertForSequenceClassification.from_pretrained("distilbert_model")
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert_model")
    return model.eval(), tokenizer

model, tokenizer = load_model()

# 📂 Load dataset
try:
    df = pd.read_excel("YC_labeled_realistic_vs_overpromisinggg.xlsx")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    st.success("Dataset loaded successfully.")
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

# 🔍 Search interface
st.title("Overpromising Pitch Detector 🔍")
st.subheader("🔎 Search a Company")
query = st.text_input("Type a company name to search").strip().lower()

if query:
    matches = df[df["company_name"].str.lower().str.contains(query, na=False)]
    if matches.empty:
        st.warning("No matching company found.")
    for _, row in matches.iterrows():
        name = row["company_name"]
        pitch = row["company_pitch"]
        st.markdown(f"### 🚀 {name}")
        st.markdown(f"<div class='pitch-box'>{pitch}</div>", unsafe_allow_html=True)

        if looks_like_gibberish(pitch):
            st.warning("❌ This doesn’t look like a proper startup pitch. Please write something meaningful. Your Pitch is too weak.")
        elif len(pitch.strip()) < 40:
            st.warning("⚠️ Your pitch is too weak. Try a stronger one.")
        else:
            inputs = tokenizer(pitch, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                logits = model(**inputs).logits
                probs = torch.softmax(logits, dim=1).squeeze()
                pred = torch.argmax(probs).item()
                confidence = probs[pred].item() * 100

            label_class = "overpromising" if pred == 1 else "realistic"
            label_text = "Overpromising ❗" if pred == 1 else "Realistic ✅"
            st.markdown(f"<div class='badge {label_class}'>{label_text}</div>", unsafe_allow_html=True)
           
# 🧪 Try your own pitch
st.subheader("🧪 Test Your Own Pitch")
user_pitch = st.text_area("Paste your startup pitch below")

if st.button("Predict My Pitch"):
    if looks_like_gibberish(user_pitch):
        st.warning("❌ This doesn’t look like a proper startup pitch. Please write something meaningful.")
    elif len(user_pitch.strip()) < 40:
        st.warning("⚠️ Your pitch is too weak. Try a stronger one.")
    else:
        inputs = tokenizer(user_pitch, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=1).squeeze()
            pred = torch.argmax(probs).item()
            confidence = probs[pred].item() * 100

        label_class = "overpromising" if pred == 1 else "realistic"
        label_text = "Overpromising ❗" if pred == 1 else "Realistic ✅"
        st.markdown(f"<div class='badge {label_class}'>{label_text}</div>", unsafe_allow_html=True)
       
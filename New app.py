import streamlit as st
import pandas as pd
import re
import tempfile
import whisper

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Timber Cubic Meter System", layout="wide")
st.title("🌲 Timber Cubic Meter Measurement System")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# ---------------- SESSION DATA ----------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Length (m)", "Girth (cm)", "Cubic Meter"]
    )

# ---------------- FUNCTIONS ----------------
def calculate_cubic(length, girth_cm):
    girth_m = girth_cm / 100
    return round(((girth_m / 4) ** 2) * length, 4)

def extract_numbers(text):
    numbers = re.findall(r"\d+\.?\d*", text)
    if len(numbers) >= 2:
        return float(numbers[0]), float(numbers[1])
    return None, None

# ---------------- MANUAL ENTRY ----------------
st.subheader("✍️ Manual Entry")

col1, col2, col3 = st.columns(3)
with col1:
    length = st.number_input("Length (meters)", step=0.01)
with col2:
    girth = st.number_input("Girth (cm)", step=0.1)
with col3:
    if st.button("Add Entry"):
        cubic = calculate_cubic(length, girth)
        st.session_state.data.loc[len(st.session_state.data)] = [
            length, girth, cubic
        ]

# ---------------- AUDIO ENTRY ----------------
st.subheader("🎤 Audio Entry (Speak the values)")

audio = st.audio_input("Speak length and girth")

if audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.getbuffer())
        audio_path = f.name

    result = model.transcribe(audio_path)
    text = result["text"]

    st.info(f"Recognized Speech: {text}")

    length_val, girth_val = extract_numbers(text)

    if length_val and girth_val:
        cubic = calculate_cubic(length_val, girth_val)
        st.session_state.data.loc[len(st.session_state.data)] = [
            length_val, girth_val, cubic
        ]
        st.success("Data added successfully from audio!")
    else:
        st.error("Could not detect length and girth clearly. Please speak again.")

# ---------------- DISPLAY TABLE ----------------
st.subheader("📊 Timber Measurement Sheet (Excel View)")

st.dataframe(st.session_state.data, use_container_width=True)

# ---------------- TOTAL ----------------
if not st.session_state.data.empty:
    total_cubic = st.session_state.data["Cubic Meter"].sum()
    st.success(f"✅ Total Cubic Meter: {total_cubic:.4f} m³")

# ---------------- EXPORT ----------------
st.subheader("⬇️ Export Data")

csv = st.session_state.data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Excel (CSV)",
    csv,
    "timber_data.csv",
    "text/csv"
)


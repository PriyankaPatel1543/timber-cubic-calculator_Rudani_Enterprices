import streamlit as st

st.set_page_config(page_title="Timber Cubic Meter Calculator")

st.title("🌲 Timber Cubic Meter Calculator")

length = st.number_input("Enter Length (in meters)", min_value=0.0, step=0.01)
girth_cm = st.number_input("Enter Girth (in cm)", min_value=0.0, step=0.1)

if st.button("Calculate"):
    girth_m = girth_cm / 100
    cubic_meter = ((girth_m / 4) ** 2) * length
    st.success(f"Cubic Meter: {cubic_meter:.4f} m³")


import streamlit as st
import numpy as np
import pandas as pd

# App Title & Layout Configuration
st.set_page_config(page_title="HIrisPlex-S HEX Translator", layout="centered")
st.title("🧬 Egyptian FDP: Genotype-to-HEX Color Translator")
st.markdown("""
This interactive web app translates custom **HIrisPlex-S multinomial logistic regression (MLR) probability inputs** 
into objective **HEX color codes**, eliminating human visual bias for intermediate eye color predictions.
""")

st.divider()

# Sidebar for Numeric Text Inputs (Replacing Sliders)
st.sidebar.header("Input Probability Values")
st.sidebar.markdown("Enter your calculated decimal probabilities (between 0.0 and 1.0):")

p_blue_input = st.sidebar.text_input("Probability: Blue (P_blue)", value="0.10")
p_inter_input = st.sidebar.text_input("Probability: Intermediate (P_intermediate)", value="0.75")
p_brown_input = st.sidebar.text_input("Probability: Brown (P_brown)", value="0.15")

# Safely parse text inputs to floats
try:
    p_blue = float(p_blue_input)
    p_inter = float(p_inter_input)
    p_brown = float(p_brown_input)
except ValueError:
    st.sidebar.error("⚠️ Please enter valid numerical decimal values (e.g., 0.15).")
    p_blue, p_inter, p_brown = 0.10, 0.75, 0.15

# Normalize probabilities so they always sum to exactly 1.0 (100%)
total = p_blue + p_inter + p_brown
if total > 0:
    p_blue_norm = p_blue / total
    p_inter_norm = p_inter / total
    p_brown_norm = p_brown / total
else:
    p_blue_norm, p_inter_norm, p_brown_norm = 0.33, 0.33, 0.34

# Define Standard RGB Color Anchors for Phenotypic Extremes
COLOR_ANCHORS = {
    'blue': np.array([70, 130, 180]),          # Steel Blue
    'intermediate': np.array([120, 140, 100]),  # Hazel / Green-Grey
    'brown': np.array([60, 40, 25])            # Dark Brown
}

def rgb_to_hex(rgb_array):
    """Converts a numpy RGB array into a standard 6-character HEX color string."""
    clipped = np.clip(rgb_array, 0, 255)
    return '#{:02x}{:02x}{:02x}'.format(int(clipped[0]), int(clipped[1]), int(clipped[2]))

# Calculate Blended RGB Vector
blended_rgb = (
    (p_blue_norm * COLOR_ANCHORS['blue']) +
    (p_inter_norm * COLOR_ANCHORS['intermediate']) +
    (p_brown_norm * COLOR_ANCHORS['brown'])
)
hex_output = rgb_to_hex(blended_rgb)

# Main Dashboard Display Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Normalized Probabilities")
    prob_df = pd.DataFrame({
        "Phenotype": ["Blue", "Intermediate", "Brown"],
        "Probability Score": [f"{p_blue_norm:.4f}", f"{p_inter_norm:.4f}", f"{p_brown_norm:.4f}"]
    })
    st.dataframe(prob_df.set_index("Phenotype"), use_container_width=True)

with col2:
    st.subheader("🎨 Objective Color Output")
    # Render dynamic color swatch box using native HTML/CSS block
    st.markdown(
        f"""
        <div style="
            background-color: {hex_output}; 
            height: 120px; 
            border-radius: 10px; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            border: 2px solid #ccc;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        ">
            <span style="color: white; font-weight: bold; font-size: 22px; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);">
                {hex_output}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.info("💡 **Project Context:** Built for Dr. Malak’s Forensic DNA Phenotyping research proposal evaluating intermediate eye color prediction across the Egypt Genome Project dataset.")

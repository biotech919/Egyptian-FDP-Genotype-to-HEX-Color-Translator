import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# App Title & Layout
st.set_page_config(page_title="HIrisPlex-S HEX Translator", layout="centered")
st.title("🧬 Egyptian FDP: Genotype-to-HEX Color Translator")
st.markdown("""
This interactive web app translates **HIrisPlex-S multinomial logistic regression (MLR) probability outputs** 
into objective **HEX color codes**, eliminating human visual bias for intermediate eye color predictions in the Egyptian population.
""")

st.divider()

# Sidebar for User Inputs (Simulating HIrisPlex-S Probability Outputs)
st.sidebar.header("Input Probability Sliders")
st.sidebar.markdown("Adjust the posterior probabilities generated from the 41-SNP panel:")

p_blue = st.sidebar.slider("Probability: Blue ($P_{\text{Blue}} $)", 0.0, 1.0, 0.10, 0.01)
p_inter = st.sidebar.slider("Probability: Intermediate ($P_{\text{Intermediate}} $)", 0.0, 1.0, 0.75, 0.01)
p_brown = st.sidebar.slider("Probability: Brown ($P_{\text{Brown}} $)", 0.0, 1.0, 0.15, 0.01)

# Normalize probabilities so they always sum to 1.0
total = p_blue + p_inter + p_brown
if total > 0:
    p_blue_norm = p_blue / total
    p_brown_norm = p_brown / total
    p_inter_norm = p_inter / total
else:
    p_blue_norm, p_inter_norm, p_brown_norm = 0.33, 0.33, 0.34

# Define RGB Color Anchors
COLOR_ANCHORS = {
    'blue': np.array([70, 130, 180]),          # Steel Blue
    'intermediate': np.array([120, 140, 100]),  # Hazel / Green-Grey
    'brown': np.array([60, 40, 25])            # Dark Brown
}

def rgb_to_hex(rgb_array):
    clipped = np.clip(rgb_array, 0, 255)
    return '#{:02x}{:02x}{:02x}'.format(int(clipped[0]), int(clipped[1]), int(clipped[2]))

# Calculate Blended RGB & HEX
blended_rgb = (
    (p_blue_norm * COLOR_ANCHORS['blue']) +
    (p_inter_norm * COLOR_ANCHORS['intermediate']) +
    (p_brown_norm * COLOR_ANCHORS['brown'])
)
hex_output = rgb_to_hex(blended_rgb)

# Main Display Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Normalized Probabilities")
    prob_df = pd.DataFrame({
        "Phenotype": ["Blue", "Intermediate", "Brown"],
        "Probability": [p_blue_norm, p_inter_norm, p_brown_norm]
    })
    st.dataframe(prob_df.set_index("Phenotype"), use_container_width=True)

with col2:
    st.subheader("🎨 Objective Color Output")
    # Display Color Swatch Block using HTML/CSS
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
        ">
            <span style="color: white; font-weight: bold; font-size: 20px; text-shadow: 1px 1px 2px black;">
                {hex_output}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.info("💡 **Project Context:** Built for Dr. Malak’s Forensic DNA Phenotyping research proposal evaluating intermediate eye color prediction across the Egypt Genome Project dataset.")
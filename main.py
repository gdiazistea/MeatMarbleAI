# main.py

import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="MeatMarbleAI", layout="centered")

st.title("🥩 MeatMarbleAI - Segmentación de carne y grasa")

uploaded_file = st.file_uploader("Subí una imagen de carne", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.image(image_np, caption="Imagen original", use_column_width=True)

    # Simulación de máscaras
    mask_carne = np.zeros(image_np.shape[:2], dtype=np.uint8)
    mask_grasa = np.zeros(image_np.shape[:2], dtype=np.uint8)

    h, w = image_np.shape[:2]
    mask_carne[h//4:h//2, w//4:w//2] = 1
    mask_grasa[h//2:h*3//4, w//2:w*3//4] = 1

    total = (mask_carne + mask_grasa).sum()
    porc_carne = mask_carne.sum() / total * 100 if total > 0 else 0
    porc_grasa = mask_grasa.sum() / total * 100 if total > 0 else 0

    # Overlay visual
    overlay = image_np.copy()
    overlay[mask_carne == 1] = [255, 0, 0]       # rojo
    overlay[mask_grasa == 1] = [255, 255, 255]   # blanco

    st.subheader("Segmentación")
    st.image(overlay, caption="Carne (rojo) / Grasa (blanco)", use_column_width=True)

    st.subheader("Resultados")
    st.metric("% Carne", f"{porc_carne:.2f}%")
    st.metric("% Grasa", f"{porc_grasa:.2f}%")

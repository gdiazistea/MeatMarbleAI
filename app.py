import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

st.title("🥩 MeatMarbleAI - Segmentación de carne y grasa")

uploaded_file = st.file_uploader("Subí una imagen de carne", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.image(image_np, caption="Imagen original", use_column_width=True)

    # Simulación de salida de modelo para desarrollo de interfaz
    mask_carne = np.zeros(image_np.shape[:2], dtype=np.uint8)
    mask_grasa = np.zeros(image_np.shape[:2], dtype=np.uint8)

    h, w = image_np.shape[:2]
    mask_carne[h//4:h//2, w//4:w//2] = 1  # zona roja simulada
    mask_grasa[h//2:h*3//4, w//2:w*3//4] = 1  # zona blanca simulada

    total = (mask_carne + mask_grasa).sum()
    porc_carne = mask_carne.sum() / total * 100 if total > 0 else 0
    porc_grasa = mask_grasa.sum() / total * 100 if total > 0 else 0

    st.subheader("Segmentación")
    overlay = image_np.copy()
    overlay[mask_carne == 1] = [255, 0, 0]   # rojo para carne
    overlay[mask_grasa == 1] = [255, 255, 255]  # blanco para grasa
    st.image(overlay, caption="Segmentación: carne (rojo), grasa (blanco)", use_column_width=True)

    st.subheader("Resultados")
    st.metric("% Carne", f"{porc_carne:.2f}%")
    st.metric("% Grasa", f"{porc_grasa:.2f}%")
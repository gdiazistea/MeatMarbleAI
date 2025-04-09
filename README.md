# 🥩 MeatMarbleAI

**MeatMarbleAI** es un proyecto de segmentación de imágenes de cortes de carne, enfocado en identificar y diferenciar regiones de **carne** y **grasa**, con el objetivo de construir un modelo de aprendizaje profundo capaz de detectar automáticamente el marmoleo (grasa intramuscular).

## 📌 ¿Qué hace este proyecto?

- Remueve el fondo de las imágenes para enfocarse únicamente en el corte de carne.
- Aplica técnicas de procesamiento en HSV para generar máscaras precisas de:
  - **Carne** (en tonos rojizos)
  - **Grasa** (en tonos claros)
- Genera un dataset de entrenamiento compatible con modelos de segmentación semántica como **DeepLabV3+**.
- Guarda las máscaras en formato PNG con clases diferenciadas por valores (0: fondo, 1: carne, 2: grasa).
- Calcula la proporción de grasa respecto al total para análisis posteriores.

## 🧠 Objetivo

Entrenar un modelo de segmentación que detecte con precisión el marmoleo en distintos tipos de cortes de carne, utilizando un dataset generado a partir de imágenes reales procesadas con técnicas de visión por computadora.

## 🚀 Próximos pasos

- Mejorar la segmentación de grasa intramuscular ajustando los valores HSV.
- Entrenar DeepLabV3+ con el dataset generado.
- Evaluar el modelo en distintos tipos de carne.
- Desarrollar una app simple para cargar una imagen y predecir automáticamente las zonas de carne y grasa.

## ⚙️ Requisitos

- Python 3.8+
- OpenCV
- NumPy
- Matplotlib
- tqdm

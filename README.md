# 🥩 MeatMarbleAI

**MeatMarbleAI** es un proyecto de segmentación de imágenes de cortes de carne, enfocado en identificar y diferenciar regiones de **carne** y **grasa**, con el objetivo de construir un modelo de aprendizaje profundo capaz de detectar automáticamente el marmoleo (grasa intramuscular). Este proyecto utiliza visión por computadora para segmentar grasa intramuscular en cortes de carne bovina tipo *ribeye* y clasificar su calidad según el sistema de la USDA (Departamento de Agricultura de EE. UU.). El objetivo es automatizar la evaluación del marmoleo, uno de los principales factores de calidad en la carne de res.

---

## 💼 Caso de Negocio
La clasificación tradicional de carne requiere inspectores capacitados que evalúan visualmente el marmoleo. Este proceso es subjetivo, costoso y poco escalable. Automatizar esta evaluación con modelos de segmentación y clasificación permite:

- Estandarizar la evaluación de calidad.
- Reducir costos operativos.
- Integrar IA en frigoríficos, mataderos y plantas de procesamiento.
- Generar reportes consistentes y trazables.


## 🧭 Contexto

La USDA clasifica la carne en varias categorías de calidad. Las principales son:

- **USDA Prime:** Marmoleo abundante.
- **USDA Choice:** Marmoleo moderado.
- **USDA Select:** Bajo marmoleo.

Estas categorías determinan el valor de mercado del corte y su uso en restaurantes o consumo general.

🔍 **Importante**:  
El marmoleo no se mide en todos los cortes, sino en una zona específica del animal: el **ribeye** entre la **12.ª y 13.ª costilla**, que actúa como indicador representativo del canal completo. Por eso, el modelo se aplica exclusivamente a imágenes de ese corte.


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

## 🔄 Pipeline del Proyecto

## 🔄 Pipeline del Proyecto

```mermaid
flowchart TD
    A[1. Imagen del Ribeye\n(corte entre costilla 12 y 13)]
    B[2. Anotación Manual\n(grasa intramuscular)]
    C[3. Entrenamiento del Modelo\n(de segmentación)]
    D[4. Segmentación Automática\n(máscara de grasa)]
    E[5. Cálculo de Métricas\n(% grasa, densidad)]
    F[6. Clasificación de Calidad\n(según USDA)]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F





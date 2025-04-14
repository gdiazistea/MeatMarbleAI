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


## 🧠 Objetivo

Entrenar un modelo de segmentación que detecte con precisión el marmoleo en distintos cortes de carne, utilizando un dataset generado a partir de imágenes reales procesadas con técnicas de visión por computadora.

## 📌 ¿Qué hace este proyecto?

- **Adquisición de Imágenes**  
  Se utilizan imágenes del corte *ribeye*, obtenidas específicamente entre la 12.ª y 13.ª costilla. Se recomienda el uso de imágenes en formato PNG con una resolución homogénea para asegurar la calidad del dataset.

- **Anotación de Grasa Intramuscular**  
  Se emplea la herramienta **Labelbox** para realizar anotaciones manuales que segmenten la grasa presente dentro del tejido muscular. Estas anotaciones permiten entrenar modelos con supervisión precisa.

- **Segmentación Automática**  
  A partir de las anotaciones, se entrena un modelo de segmentación semántica (por ejemplo, **U-Net** o **DeepLabV3+**) que identifica automáticamente las regiones de grasa intramuscular en nuevas imágenes.

- **Cálculo de Métricas**  
  Una vez segmentadas las imágenes, se calcula la proporción de grasa respecto al área total del músculo, así como la densidad y la distribución de los islotes grasos. Estas métricas son clave para la evaluación objetiva del marmoleo.

- **Clasificación según USDA**  
  Basándose en las métricas extraídas, se realiza una predicción de la calidad del corte conforme a los estándares del sistema USDA:  
  - ≥13% de grasa → **USDA Prime**  
  - 4–13% de grasa → **USDA Choice**  
  - <4% de grasa → **USDA Select**

- **Aplicaciones y Visualización**  
  Los resultados pueden ser utilizados en sistemas automatizados de inspección, visualizados mediante dashboards o integrados en procesos de aseguramiento de calidad industrial.


## 🔄 Pipeline del Proyecto

El siguiente diagrama muestra el flujo de trabajo del proyecto, desde la adquisición de imágenes hasta la clasificación de calidad según los estándares USDA:

```mermaid
flowchart TD
    Start([Inicio])
    
    A[Imagen del Ribeye<br/>(costilla 12-13)]
    B[Anotación Manual<br/>(grasa intramuscular)]
    C[Entrenamiento del Modelo<br/>de Segmentación]
    D[Segmentación Automática<br/>(máscara de grasa)]
    E[Cálculo de Métricas<br/>(% grasa, densidad)]
    F[Clasificación USDA<br/>(Prime / Choice / Select)]
    
    End([Fin])
    
    Start --> A
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> End
```



# Metodología del Modelo

## 1. Contexto

Este proyecto utiliza un conjunto de datos sintético de viviendas ubicadas en Lima Metropolitana. Los datos fueron generados con fines académicos para practicar herramientas y buenas prácticas de Ciencia de Datos, incluyendo Git, GitHub, GitHub Actions y automatización de flujos de trabajo.

---

## 2. Variables de Entrada

Las variables utilizadas como predictores del modelo son las siguientes:

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `area_m2` | Numérica | Área de la vivienda en metros cuadrados. |
| `habitaciones` | Entera | Número de habitaciones de la vivienda. |
| `banos` | Entera | Número de baños de la vivienda. |
| `antiguedad_anos` | Numérica | Antigüedad de la vivienda en años. |
| `distrito_cod` | Entera | Código numérico asignado al distrito. |

---

## 3. Variable Objetivo

La variable que se busca predecir es:

| Variable | Descripción |
|----------|-------------|
| `precio_usd` | Precio estimado de la vivienda en dólares estadounidenses. |

---

## 4. Preprocesamiento de Datos

El flujo de preparación de datos contempla las siguientes etapas:

1. Eliminación de valores nulos.
2. Eliminación de registros con precios negativos.
3. Eliminación de áreas no válidas o inconsistentes.
4. Codificación numérica de la variable categórica `distrito`.
5. Escalamiento de variables numéricas para facilitar el entrenamiento del modelo.

---

## 5. Modelo Utilizado

El modelo empleado es **Random Forest Regressor** (`RandomForestRegressor`) de la biblioteca **scikit-learn**.

Random Forest es un algoritmo de aprendizaje supervisado basado en un conjunto de árboles de decisión. La predicción final se obtiene mediante la agregación de múltiples árboles, lo que permite reducir la varianza y mejorar la capacidad de generalización respecto a un único árbol de decisión.

---

## 6. Métricas de Evaluación

El desempeño del modelo se evalúa mediante las siguientes métricas:

| Métrica | Significado |
|----------|-------------|
| **MAE** | Error Absoluto Medio (Mean Absolute Error), expresado en dólares. |
| **R²** | Coeficiente de Determinación, que representa la proporción de variabilidad explicada por el modelo. |

---

## 7. Limitaciones

Este proyecto presenta las siguientes limitaciones:

- El conjunto de datos utilizado es sintético.
- Las métricas obtenidas no representan el comportamiento real del mercado inmobiliario de Lima Metropolitana.
- El objetivo principal del proyecto es practicar herramientas de desarrollo colaborativo y automatización en proyectos de Ciencia de Datos, no construir un modelo inmobiliario de uso productivo.
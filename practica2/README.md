## 1. Resumen

Este proyecto consiste en desarrollar un análisis de datos integral mediante un entorno interactivo (Jupyter Notebook) en Python. Utilizando un conjunto de datos proporcionado sobre cursos disponibles en la plataforma Coursera, junto con un archivo de texto adicional, se ejecutan tareas de limpieza, transformación, visualización estadística y análisis textual. El objetivo central es proporcionar insights valiosos sobre la oferta educativa de la plataforma, aplicando herramientas modernas como Pandas, NumPy, Matplotlib y NLTK.

## 2. Objetivos de Aprendizaje

### Objetivo General
- Desarrollar una solución de análisis de datos con Python, enfocada en manipulación, visualización y análisis textual.

### Objetivos Específicos
- Realizar limpieza y transformación de datos con Pandas.
- Aplicar análisis estadístico básico utilizando NumPy.
- Generar visualizaciones claras mediante Matplotlib.
- Implementar técnicas de procesamiento de lenguaje natural (NLP) con NLTK.
- Presentar resultados de manera clara y documentada.

## 3. Metodología
- **Limpieza y Transformación:** Se utilizaron funciones de Pandas para tratar datos faltantes, eliminar duplicados y normalizar la información.
- **Cálculo de Métricas:** Se aplicaron métodos estadísticos con NumPy para determinar calificaciones promedio, ratings extremos y porcentajes relevantes.
- **Visualizaciones:** Se elaboraron gráficos informativos utilizando Matplotlib para facilitar la interpretación visual de los resultados.
- **Análisis Textual (NLP):** Se empleó NLTK para analizar un archivo textual mediante técnicas de tokenización, stemming, lematización, stopwords, frecuencia de palabras, análisis de sentimientos y reconocimiento de entidades nombradas.

## 4. Desarrollo del Análisis

### 4.1 Limpieza y transformación del dataset
Se eliminaron registros con datos faltantes y duplicados, se corrigieron inconsistencias en tipos de datos, y se realizó normalización de formatos para facilitar el análisis posterior.

### 4.2 Análisis estadístico
- **Calificaciones promedio:** Se determinó que la calificación promedio global de los cursos es de 4.5.
- **Curso con mayor rating:** "Machine Learning" con rating 4.9.
- **Curso con menor rating:** "Introduction to Philosophy" con rating 3.7.
- **Cursos con horario flexible:** El 78% de los cursos ofrecen un horario flexible.

### 4.3 Visualizaciones
- **Gráfica de barras (cursos por nivel):** La mayoría de cursos pertenecen al nivel Principiante (45%), seguido de Intermedio (35%) y Avanzado (20%).
![Cursos por nivel](./docs/src/Numero%20de%20cursos%20por%20nivel%20de%20dificultad.png)
- **Gráfica horizontal ( cursos por categoría):** Las categorías con más cursos son Data Science y Negocios, representando el 40% del total.
![Cursos por categoría](./docs/src/Numero%20de%20cursos%20por%20categoria.png)
- **Gráfico de dispersión (duración vs. número de revisiones):** Cursos más extensos no necesariamente reciben más revisiones, lo que indica que la duración no afecta significativamente la popularidad.
![Duracion vs numero de revisiones](./docs/src/Relacion%20entre%20duracion%20del%20curso%20y%20numero%20de%20revisiones.png)
- **Histograma (duración de cursos):** La duración media de los cursos es aproximadamente de 4 semanas.
![Duracion de cursos](./docs/src/Distribución%20de%20la%20duración%20de%20los%20cursos.png)
- **Boxplot (calificaciones por dificultad):** Los cursos avanzados muestran una mayor variabilidad en las calificaciones comparados con cursos principiantes e intermedios.
![Calificaciones por dificultad](./docs/src/Duración%20de%20calificaciones%20por%20nivel%20de%20dificultad.png)

### 4.4 Análisis textual (NLP)
- **Tokenización:** Se realizó una segmentación del texto en palabras individuales.
- **Stemming y Lematización:** Se normalizaron términos a su raíz o lema básico para reducir la variabilidad.
- **Stopwords:** Se eliminaron palabras frecuentes que no aportan información significativa (artículos, preposiciones, etc.).
- **Frecuencia de palabras:** Las palabras más frecuentes son "data", "analysis" y "python", indicando claramente el tema central del texto analizado.
![Frecuencia de palabras](./docs/src/Frecuencia%20de%20las%2030%20palabras%20más%20comunes.png)
- **Análisis de sentimientos:** El texto tiene predominancia de sentimiento positivo (62%), neutral (28%) y negativo (10%).
![Analisis de sentimientos](./docs/src/Analisis%20de%20sentimientos.png)
- **Reconocimiento de entidades nombradas:** Se identificaron entidades como Coursera, Python, Google y Microsoft, destacando actores clave del contenido textual.
![Reconocimiento de entidades nombradas](./docs/src/Nube%20de%20palabras.png)

## 5. Conclusiones

El análisis estadístico reveló insights significativos sobre la oferta educativa en Coursera, destacando preferencia hacia cursos de nivel principiante e intermedio, especialmente en categorías tecnológicas como Data Science y Negocios. Las visualizaciones apoyaron efectivamente la interpretación rápida y clara de estos resultados.

El análisis textual proporcionó detalles adicionales sobre el contenido relacionado con análisis de datos y Python, confirmando el enfoque positivo hacia la temática abordada.

Finalmente, el uso de Python demostró ser extremadamente eficiente y adecuado para estas tareas debido a la potencia y versatilidad de sus librerías especializadas.


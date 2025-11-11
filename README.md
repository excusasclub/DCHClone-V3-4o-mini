# DchBrain SEO Rewriter · Sistema de reescritura y mejora automática de contenido por URL

**DchBrain SEO Rewriter** es un sistema modular en **Python** diseñado para reescribir y mejorar de forma masiva el contenido de un sitio web a partir de un estudio de palabras clave exportado desde herramientas SEO como **Semrush**, **Ahrefs** o similares.

A diferencia de un simple generador de artículos, este proyecto:

- Parte de un **CSV real** de rendimiento SEO por URL.  
- **Agrupa las keywords** de cada página.  
- **Descarga el contenido actual** de esas URLs.  
- **Lo reescribe con IA (GPT-4o-mini)**, aplicando prompts totalmente editables.  
- **Enriquece cada artículo con:**
  - Título optimizado  
  - Estructura en HTML (H2, H3)  
  - Cuerpo completo  
  - Categoría  
  - Slug  
  - Autor  
  - Fecha de publicación  
  - Portada descargada  
  - Vídeo de YouTube insertado  

Al final, obtienes un CSV listo para importar a un CMS (WordPress, PrestaShop, etc.) o para atacar una API propia.

--- ✦ ---

**DchBrain SEO Rewriter** 

1. Tu CSV de estudio de keywords.  
2. El contenido real de cada URL.  
3. Tus reglas de redacción (definidas en los prompts).  

Y te devuelve un conjunto de artículos reescritos y enriquecidos listos para publicar.

--- ✦ ---

## Flujo de trabajo completo

El flujo se organiza en scripts numerados.  

Cada uno consume la salida del anterior:
- _0. Unificar.py
- _1. Scrapear.py
- _2. Redactor.py
- _3. Fechas.py
- _4. Portadas.py
- _5. YouTube.py

### 1. Unificación de keywords por URL  
**Archivo:** `_0. Unificar.py`

**Entrada:**  
`2. Original.csv`, un CSV exportado desde Semrush/Ahrefs con columnas típicas como:

- Keyword  
- Position  
- Search Volume  
- URL  
- etc.

**Qué hace:**

- Agrupa las filas por columna `URL`.  
- Junta todas las `Keyword` de esa URL en una sola celda separadas por saltos de línea.

**Salida:**

`3. Unificado.csv` con:  
- `URL`  
- `Keywords` (todas las keywords que apuntan a esa URL, una por línea)

**Propósito:**  
Pasar de “keyword individual” a “cluster de búsqueda por URL”, que es como de verdad se trabaja el contenido on-page.

--- ✦ ---

### 2. Scrapear el contenido real de cada URL  
**Archivo:** `_1. Scrapear.py`

**Entrada:**  
`3. Unificado.csv`

**Qué hace:**

Para cada fila:

- Lee la `URL`.  
- Usa `newspaper3k` para:
  - Descargar la página.  
  - Extraer el título del artículo.  
  - Extraer el texto principal limpio.  
  - Detectar la imagen principal.  

Guarda los resultados en un nuevo CSV.

**Salida:**  
`4. Scrapeado.csv` con columnas:  

- URL  
- Keywords  
- Titulo  
- Contenido  
- Portada  

**Propósito:**  
Crear una versión “digerible” del sitio actual: título + cuerpo de texto + imagen por URL.  
Esta base se entrega a la IA para reescribir.

--- ✦ ---

### 3. Reescritura y enriquecimiento con IA  
**Archivo:** `_2. Redactor.py`

Es el núcleo del sistema. Aquí se combina todo:

- Keywords por URL.  
- Contenido scrapeado.  
- Prompts personalizados.  
- Modelo **GPT-4o-mini**.

#### Entradas

- `4. Scrapeado.csv`  
- `0. OpenAI.txt`  
  - Lista de claves de API, una por línea (permite rotación y repartir carga).  
- `1. Autores.txt`  
  - Lista de autores disponibles (uno se asigna aleatoriamente a cada artículo).  
- Directorios de prompts:
  - `0. Sistema`
  - `1. Usuario`
  - `2. Asistente`
  Cada uno contiene:
  - `0. Titulo.txt`
  - `1. Resumen.txt`
  - `2. Estructura.txt`
  - `3. Articulo.txt`
  - `4. Categoria.txt`

#### Lógica principal

##### Rotación de API keys  
El script mantiene un índice global y va rotando por las claves de `0. OpenAI.txt`.  
Cada llamada usa una clave distinta; si hay un error, pasa a la siguiente.

##### Prompts por rol  
Cada parte del contenido usa tres contextos:
- **system** → reglas globales, tono, estilo, formato.  
- **user** → datos concretos (keywords, contenido original).  
- **assistant** → ejemplos, tono y matices.

Esto se aplica para:
- Título  
- Resumen  
- Estructura  
- Artículo  
- Categoría  

##### Generación de cada campo

- **`crear_titulo(keywords, titulo_original)`**  
  Combina keywords + título scrapeado.  
  Usa un prompt SEO.  
  Si supera 70 caracteres, se acorta.  
  Elimina puntos finales.

- **`crear_resumen(contenido)`**  
  Resume el texto scrapeado.  
  Sirve de base para los siguientes pasos.

- **`crear_estructura(titulo, resumen)`**  
  Genera encabezados H2/H3 y secciones principales.

- **`crear_articulo(titulo, resumen, estructura, keywords)`**  
  Redacta el artículo completo en HTML.  
  Corrige frases redundantes (“En conclusión”, “En resumen”).  
  Ajusta jerarquías de encabezados.

- **`crear_categoria(titulo)`**  
  Clasifica el artículo según el tema.

- **`crear_slug(keywords)`**  
  Toma la primera keyword, normaliza acentos y ñ, convierte espacios en guiones.

- **`crear_autor()`**  
  Selecciona un autor aleatorio de `1. Autores.txt`.

##### Concurrencia  
Usa `ThreadPoolExecutor` con muchos hilos para procesar varias filas en paralelo.  
Controla qué keywords ya están procesadas mediante lectura previa de `5. Redactado.csv`.

#### Salida

`5. Redactado.csv` con columnas:

- URL  
- Keywords  
- Titulo  
- Contenido (HTML)  
- Portada  
- Categoria  
- SLUG  
- Autor  

--- ✦ ---

### 4. Asignación de fechas de publicación  
**Archivo:** `_3. Fechas.py`

**Entrada:**  
`5. Redactado.csv`

**Qué hace:**

- Cuenta los artículos.  
- Define un calendario desde `2024-01-01`.  
- Calcula, por mes y semana, cuántos artículos publicar al día.  
- Genera fechas y horas aleatorias entre 07:00 y 22:59.  
- Añade una columna `Fecha` y sobrescribe el archivo.

**Salida:**  
`5. Redactado.csv` con una nueva columna `Fecha (YYYY-MM-DD HH:MM:SS)`.

**Usos:**

- Planificación de publicación automática.  
- Simulación de histórico editorial.

--- ✦ ---

### 5. Descarga de portadas  
**Archivo:** `_4. Portadas.py`

**Entrada:**  
`5. Redactado.csv`

**Qué hace:**

- Comprueba la existencia de `3. Portadas/` (la crea si falta).  
- Recorre las URLs de imágenes de la columna `Portada`.  
- Descarga cada imagen con `requests`.  
- Guarda en `3. Portadas/` usando el nombre original.  
- Usa `ThreadPoolExecutor` con 32 hilos.

**Salida:**  
Carpeta `3. Portadas/` con las imágenes principales de los artículos.

--- ✦ ---

### 6. Inserción de vídeos de YouTube  
**Archivo:** `_5. YouTube.py`

**Entrada:**  
`5. Redactado.csv`

**Qué hace:**

- Carga el CSV.  
- Añade una nueva columna `Video`.  
- Para cada fila:
  - Toma la primera keyword.
  - Lanza Chrome en modo headless con Selenium.
  - Busca en YouTube esa keyword.
  - Extrae el primer `video_id` de los resultados.
  - Si lo encuentra:
    - Genera un iframe con `https://www.youtube.com/embed/{video_id}`.
    - Lo añade a la columna `Video`.
  - Si no, deja el campo vacío.
- Reescribe el CSV con la columna nueva.

**Salida:**  
`5. Redactado.csv` con la columna adicional `Video (iframe HTML)`.

**Resultado:**  
Cada artículo queda enlazado a un vídeo relevante de YouTube, mejorando la experiencia y el tiempo en página.

--- ✦ ---

## Estructura del proyecto


```text
.
│ 0. OpenAI.txt ← Claves de la API de OpenAI
│ 1. Autores.txt ← Lista de autores
│ 2. Original.csv ← Estudio SEO exportado
│ _0. Unificar.py
│ _1. Scrapear.py
│ _2. Redactor.py
│ _3. Fechas.py
│ _4. Portadas.py
│ _5. YouTube.py
│ _6. Probador.html
│
├── 0. Sistema ← Prompts del rol "system"
├── 1. Usuario ← Prompts del rol "user"
├── 2. Asistente ← Prompts del rol "assistant"
├── 3. Portadas ← Imágenes descargadas
└── 4. Editadas ← Artículos revisados manualmente
```

--- ✦ ---

## Requisitos y dependencias

Versión de Python recomendada:

Python 3.10 o superior.

--- ✦ ---

### Dependencias principales:

- pandas

- requests

- newspaper3k

- openai

- selenium

- chromedriver (instalado y disponible en PATH)


```bash
pip install -r requirements.txt
```

--- ✦ ---

## Ejecución del pipeline

Ejemplo de ejecución del flujo completo, en este orden:

```text
python "_0. Unificar.py"

python "_1. Scrapear.py"

python "_2. Redactor.py"

python "_3. Fechas.py"

python "_4. Portadas.py"

python "_5. YouTube.py"
```

En cada paso se genera o actualiza un archivo:

De 2. Original.csv se pasa a 3. Unificado.csv.

De 3. Unificado.csv se pasa a 4. Scrapeado.csv.

De 4. Scrapeado.csv se pasa a 5. Redactado.csv.

Y 5. Redactado.csv se enriquece con:

- Columna Fecha.

- Descarga de portadas.

- Columna Video.

--- ✦ ---

## Archivos de salida y propósito
```text
Archivo / carpeta	Descripción
3. Unificado.csv	Keywords agrupadas por URL
4. Scrapeado.csv	Contenido original de las páginas (título, cuerpo, portada)
5. Redactado.csv	Artículos reescritos y enriquecidos con IA
3. Portadas/	Imágenes descargadas de las URLs de portada
```
--- ✦ ---

## Personalización mediante prompts

El comportamiento del modelo no está “hardcodeado” en el Python. Está externalizado en:

0. Sistema

1. Usuario

2. Asistente

Cada carpeta contiene:

0. Titulo.txt

1. Resumen.txt

2. Estructura.txt

3. Articulo.txt

4. Categoria.txt

Modificando esos archivos puedes:

- Cambiar completamente el tono (más técnico, más cercano, más comercial).

- Ajustar la longitud objetivo de los textos.

- Definir una estructura fija (por ejemplo, siempre X H2, con listas, etc.).

- Forzar el uso de ciertas llamadas a la acción.

- Ajustar el tipo de categorías generadas.

- No hace falta tocar el código para cambiar el estilo del contenido. Solo se modifican estos .txt.

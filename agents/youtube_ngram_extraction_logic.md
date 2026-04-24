# Especificacion de Logica de Extraccion de N-gramas de YouTube

Este documento detalla la funcionalidad, reglas de negocio y estructura de datos de la herramienta de extraccion y analisis de frases (n-gramas) de YouTube.

## Objetivo
La herramienta permite identificar frases recurrentes (de 2 a 6 palabras) en los videos de creadores de contenido especificos. Utiliza procesamiento en paralelo para la descarga de transcripciones y el analisis estadistico, permitiendo diferenciar entre frases populares (Union) y frases caracteristicas que aparecen en la mayoria de sus videos (Interseccion).

## Inputs
La herramienta recibe un diccionario de Python donde la Key es la URL del video de YouTube y el Value es el nombre del creador.
Ejemplo:
```python
{
    "https://www.youtube.com/watch?v=vId1": "CREADOR_A",
    "https://www.youtube.com/watch?v=vId2": "CREADOR_B"
}
```

## Reglas de Negocio y Funcionalidad

### Etapa 1: Descarga (Stage 1)
- Extraccion de ID: Se limpian las URLs para obtener el ID de 11 caracteres.
- Descarga Paralela: Se utiliza concurrent.futures.ThreadPoolExecutor para descargar multiples transcripciones simultaneamente.
- Idiomas: Intenta obtener la transcripcion en español (es) y, si no esta disponible, en ingles (en).
- Persistencia Temporal: Guarda los datos crudos (transcripcion + metadatos) en archivos JSON individuales por video.

### Etapa 2: Procesamiento (Stage 2)
- Limpieza de Texto: Convierte a minusculas y elimina signos de puntuacion.
- Tokenizacion con Timestamps (Manejo Multi-bloque): La herramienta descompone la transcripcion completa en una lista plana de palabras (tokens). Cada token conserva el tiempo de inicio y fin de su bloque original. Esto permite que un n-grama pueda formarse con palabras que pertenecen a diferentes cuadros de texto (objetos de la transcripcion original) de forma fluida.
- Continuidad Temporal: Al generar un n-grama que cruza bloques, el tiempo de inicio se toma del primer token del n-grama y el tiempo de fin del ultimo token, garantizando precision en la marca de tiempo de la frase completa.
- Generacion de N-gramas: Genera combinaciones de 2, 3, 4, 5 y 6 palabras consecutivas.
- Filtro de Stopwords: Un n-grama es descartado solo si todas las palabras que lo componen son stopwords (ej. "de la", "y el"). Si contiene al menos una palabra con valor semantico, se mantiene.
- Metricas de Analisis:
    - Union: Representa la frecuencia absoluta de la frase en todo el set de videos.
    - Interseccion: Frases que aparecen en un porcentaje igual o mayor al INTERSECTION_THRESHOLD (actualmente 60%) del total de videos procesados para ese creador.
- Modos de Salida:
    - first_appearance: Solo registra la primera vez que se escucho la frase y el total de repeticiones.
    - all_appearances: Registra cada una de las veces que se dijo la frase con su URL y marca de tiempo especifica.

## Estructura de Archivos (Output)

El proyecto genera una jerarquia de carpetas bajo processed_files/:

```text
processed_files/
├── processed_transcriptions/          # Transcripciones crudas por creador
│   ├── GUSGRI/
│   │   ├── videoId1.json
│   │   └── videoId2.json
│   └── XOCAS/
│       └── ...
└── processed_n_gramas/                # Resultados del analisis
    ├── creators/                      # Resultados individuales
    │   ├── GUSGRI/
    │   │   ├── all_appearances/       # Detalle de cada aparicion
    │   │   │   ├── n_gramas_interception.json
    │   │   │   └── n_gramas_union.json
    │   │   └── first_appearance/      # Resumen (primera aparicion)
    │   │       ├── n_gramas_interception.json
    │   │       └── n_gramas_union.json
    │   └── XOCAS/
    │       └── ...
    └── global/                        # Agregados de todos los creadores
        ├── all_appearances/
        │   ├── n_gramas_interception.json
        │   └── n_gramas_union.json
        └── first_appearance/
            ├── n_gramas_interception.json
            └── n_gramas_union.json
```

## Formato de Datos (JSON)

### n_gramas_union.json (Ejemplo first_appearance)
```json
{
  "2_grams": [
    {
      "phrase": "hola que",
      "repetitions": 15,
      "first_appearance": {
        "start": 10.5,
        "end": 12.0,
        "url": "..."
      }
    }
  ]
}
```

### n_gramas_union.json (Ejemplo all_appearances)
```json
{
  "2_grams": [
    {
      "phrase": "hola que",
      "repetitions": 15,
      "appearances": [
        { "start": 10.5, "end": 12.0, "url": "..." },
        { "start": 150.2, "end": 151.5, "url": "..." }
      ]
    }
  ]
}
```

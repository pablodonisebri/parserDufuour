# parserDufuour

## Introducción
Es una API para automatizar la obtención de lecturas bíblicas asociadas a una palabra en el libro Dufour en su versión online, disponible en [hjg.com.ar/vocbib](https://hjg.com.ar/vocbib/). La API extrae automáticamente las lecturas desde la página correspondiente (en caso de existir) y las organiza en un archivo Excel con columnas ordenadas por lectura (1a, 2a, 3a o Evangelio).

## Características
- Extrae las lecturas bíblicas asociadas a una palabra del libro Dufour en línea.
- Procesa y clasifica las citas en categorías:
  - **1a Lectura**: Libros del Antiguo Testamento (Torá e históricos)
  - **2a Lectura**: Libros del Antiguo Testamento (sapienciales y proféticos)
  - **3a Lectura**: Cartas del Nuevo Testamento
  - **Evangelio**: Los cuatro Evangelios
- Genera un archivo Excel (`.xlsx`) con las lecturas organizadas en columnas.
- Proporciona endpoints REST para obtener las lecturas en formato JSON o generar archivos Excel.

## Uso con Docker

### Construir la imagen Docker
```bash
docker build -t parser-dufour .
```

### Ejecutar el contenedor
```bash
docker run -d -p 8000:8000 -v ${PWD}:/app --name dufour-service parser-dufour
```

La API estará disponible en `http://localhost:8000`

## Endpoints de la API

### GET /lecturas/{palabra}
Genera un archivo Excel con las lecturas bíblicas en el servidor local y retorna código de estado de éxito.

**Parámetros:**
- `palabra` (string): La palabra clave a buscar

**Respuesta:**
- Código HTTP 200 si el archivo se generó correctamente
- El archivo Excel se guarda localmente en el servidor como `lecturas_{palabra}.xlsx`

### GET /lecturas/{palabra}/excel
Descarga un archivo Excel con las lecturas organizadas en columnas.

**Parámetros:**
- `palabra` (string): La palabra clave a buscar

**Respuesta:**
Archivo Excel (`lecturas_{palabra}.xlsx`) para descarga.

## Funcionamiento técnico
1. **Obtención de la página web**: Se accede a la URL específica de la palabra en `https://hjg.com.ar/vocbib/art/<palabra>.html`.
2. **Extracción de citas**: Se analizan los contenidos HTML y se buscan las citas encerradas entre los tags `<cite>...</cite>` mediante expresiones regulares.
3. **Normalización de citas**: Algunas citas pueden no incluir el nombre del libro, por lo que se asigna el último libro identificado en caso necesario.
4. **Clasificación**: Se comparan las citas con las listas de libros categorizados previamente y se asignan a su respectiva categoría (1a, 2a, 3a o Evangelio).
5. **Generación del archivo Excel**: Se crea un archivo `lecturas_<palabra>.xlsx` con las lecturas ordenadas en columnas.

## Salida del programa
La API puede generar:
- **Código de estado HTTP 200** cuando se genera exitosamente el archivo Excel en el servidor
- **Archivo Excel** con las siguientes columnas:
  - **1a Lectura** (Primera Lectura)
  - **2a Lectura** (Segunda Lectura)
  - **3a Lectura** (Tercera Lectura)
  - **Evangelio**

Cada columna contendrá la lista de citas bíblicas organizadas por su tipo de lectura.

## Manejo de errores
- Si la página web no se puede obtener, se retorna un error HTTP 404.
- Si las citas no incluyen el nombre del libro, se asigna el último identificado.
- La API retorna códigos de estado HTTP apropiados para diferentes tipos de errores.


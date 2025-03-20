# parserDufuour

## Introducción
 Es una herramienta para automatizar la obtención de lecturas bíblicas asociadas a una palabra en el libro Dufour en su versión online, disponible en [hjg.com.ar/vocbib](https://hjg.com.ar/vocbib/). La herramienta extrae automáticamente las lecturas desde la página correspondiente (en caso de existir) y las organiza en un archivo Excel con columnas ordenadas por lectura (1a, 2a, 3a o Evangelio).

## Características
- Extrae las lecturas bíblicas asociadas a una palabra del libro Dufour en línea.
- Procesa y clasifica las citas en categorías:
  - **1a Lectura**: Libros del Antiguo Testamento (Torá e históricos)
  - **2a Lectura**: Libros del Antiguo Testamento (sapienciales y proféticos)
  - **3a Lectura**: Cartas del Nuevo Testamento
  - **Evangelio**: Los cuatro Evangelios
- Genera un archivo Excel (`.xlsx`) con las lecturas organizadas en columnas.

## Uso
Ejecuta el programa e introduce la palabra que deseas buscar:
```bash
python main.py
```
El programa pedirá que ingreses una palabra clave y automáticamente extraerá las lecturas correspondientes, generando un archivo Excel con el nombre `lecturas_<palabra>.xlsx`.

### Código principal (`main.py`)
```python
from cite_categorizer.categorizer import CiteCategorizer

def main():
    palabra = input("Enter the keyword (palabra): ").strip().lower().replace(" ", "_")
    categorizer = CiteCategorizer(palabra)
    categorizer.run()

if __name__ == "__main__":
    main()
```

## Funcionamiento técnico
1. **Obtención de la página web**: Se accede a la URL específica de la palabra en `https://hjg.com.ar/vocbib/art/<palabra>.html`.
2. **Extracción de citas**: Se analizan los contenidos HTML y se buscan las citas encerradas entre los tags `<cite>...</cite>` mediante expresiones regulares.
3. **Normalización de citas**: Algunas citas pueden no incluir el nombre del libro, por lo que se asigna el último libro identificado en caso necesario.
4. **Clasificación**: Se comparan las citas con las listas de libros categorizados previamente y se asignan a su respectiva categoría (1a, 2a, 3a o Evangelio).
5. **Generación del archivo Excel**: Se crea un archivo `lecturas_<palabra>.xlsx` con las lecturas ordenadas en columnas.

## Salida del programa
El programa genera un archivo Excel con las siguientes columnas:
- **1a Lectura** (Primera Lectura)
- **2a Lectura** (Segunda Lectura)
- **3a Lectura** (Tercera Lectura)
- **Evangelio**

Cada columna contendrá la lista de citas bíblicas organizadas por su tipo de lectura.

## Manejo de errores
- Si la página web no se puede obtener, se muestra un mensaje de error.
- Si las citas no incluyen el nombre del libro, se asigna el último identificado.

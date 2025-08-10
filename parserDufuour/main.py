from cite_categorizer.categorizer import CiteCategorizer
from fastapi import FastAPI,  HTTPException
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Dufuour API",
    version="1.0.0",
    description="Una API para devolver las lecturas de una palabra dada en el Dufuour."
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
)

categorizer = CiteCategorizer()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cite Categorizer API"}


@app.get("/palabras")
def read_palabras():
    try:
        palabras = categorizer.get_list_lecturas()

        return {"palabras": palabras}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/lecturas/{word}")
def categorize_citation(word: str):
    word = categorizer.normalize_word(word)

    file_path = os.path.join("/var/tmp/lecturas", f"lecturas_{word}.xlsx")
    try:
        if os.path.exists(file_path):
            return {"message": f"Citation already categorized for word: {word}"}

        categorizer.run(word)
        return {"message": f"Citation successfully categorized for word: {word}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/lecturas/{word:path}/excel")
def categorize_citation_and_export_pdf(word: str):
    word = categorizer.normalize_word(word)
    excel_path = os.path.join("/var/tmp/lecturas", f"lecturas_{word}.pdf")

    try:
        # Si ya existe el PDF, lo devolvemos directamente
        if os.path.exists(excel_path):
            return FileResponse(excel_path, media_type='application/pdf', filename=f"lecturas_{word}.pdf")

        # Generar Excel y extraer DataFrame para crear PDF
        categorizer.run(word)  # Asumo que crea Excel

        if not os.path.exists(excel_path):
            raise HTTPException(
                status_code=404, detail=f"Excel file not found: {excel_path}")

        categorizer.run(word)

        if not os.path.exists(excel_path):
            raise HTTPException(
                status_code=500, detail=f"PDF file not created: {excel_path}")

        return FileResponse(excel_path, media_type='application/pdf', filename=f"lecturas_{word}.pdf")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

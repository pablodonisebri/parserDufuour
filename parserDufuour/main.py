from cite_categorizer.categorizer import CiteCategorizer
from fastapi import FastAPI,  HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="Dufuour API",
    version="1.0.0",
    description="Una API para devolver las lecturas de una palabra dada en el Dufuour."
)


categorizer = CiteCategorizer()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cite Categorizer API"}


@app.get("/lecturas/{word}")
def categorize_citation(word: str):
    file_path = os.path.join("/var/tmp/lecturas", f"lecturas_{word}.xlsx")
    try:
        if os.path.exists(file_path):
            return {"message": f"Citation already categorized for word: {word}"}

        categorizer.run(word)
        return {"message": f"Citation successfully categorized for word: {word}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/lecturas/{word}/excel")
def categorize_citation_and_export(word: str):
    file_path = os.path.join("/var/tmp/lecturas", f"lecturas_{word}.xlsx")
    try:
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=f"lecturas_{word}.xlsx")

        categorizer.run(word)

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, detail=f"File not found: {file_path}")

        return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=f"lecturas_{word}.xlsx")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

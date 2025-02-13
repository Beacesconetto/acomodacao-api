from fastapi import FastAPI, HTTPException, Query
import json

app = FastAPI()

DATA_FILE = "acomodacoes.json"

def load_files():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_files(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)

@app.get("/acomodacoes")
def  list_all_accommodations():
    return load_files()

@app.get("/acomodacoes/filtrar")
def filter_accommodations_by_city(cidade: str = Query(..., description="Filtrar por cidade")):
    dados = load_files()
    filtradas = [a for a in dados if cidade.lower() in a["cidade"].lower()]
    return filtradas

@app.get("/acomodacoes/{id}")
def get_accommodations(id: int):
    dados = load_files()
    for a in dados:
        if a["id"] == id:
            return a
    raise HTTPException(status_code=404, detail="Acomodação não encontrada")


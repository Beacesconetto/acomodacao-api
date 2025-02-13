from fastapi import FastAPI, HTTPException, Query
import json

app = FastAPI()

DATA_FILE = "acomodacoes.json"

def carregar_dados():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)

@app.get("/acomodacoes")
def listar_todas_acomodacoes():
    return carregar_dados()

@app.get("/acomodacoes/filtrar")
def filtrar_acomodacoes_por_cidade(cidade: str = Query(..., description="Filtrar por cidade")):
    dados = carregar_dados()
    filtradas = [a for a in dados if cidade.lower() in a["cidade"].lower()]
    return filtradas

@app.get("/acomodacoes/{id}")
def obter_acomodacao(id: int):
    dados = carregar_dados()
    for a in dados:
        if a["id"] == id:
            return a
    raise HTTPException(status_code=404, detail="Acomodação não encontrada")


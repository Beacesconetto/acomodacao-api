from fastapi import FastAPI, HTTPException, Query
import json
from dotenv import load_dotenv
import os
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Accommodation(BaseModel):
    name: str
    image: str
    location: str
    price: float


load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accommodations (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        image TEXT NOT NULL,
        location TEXT NOT NULL,
        price REAL NOT NULL
    )
""")
conn.commit()

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
def list_all_accommodations():
    try:
        cursor.execute("SELECT id, name, image, location, price FROM accommodations")
        acomodacoes = cursor.fetchall()

        result = [
            {"id": a[0], "name": a[1], "image": a[2],"location": a[3], "price": a[4]}
            for a in acomodacoes
        ]

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar do banco: {str(e)}")


@app.get("/acomodacoes/filtrar")
def filter_accommodations_by_location(cidade: str = Query(..., description="Filtrar por cidade")):
    '''
    Essa função não será usada no front-end para que ele não faça 
    várias consultas ao banco de dados. Para filtrar as cidades o front irá utilizar
    a rota /acomodacoes
    '''
    dados = load_files()
    filtradas = [a for a in dados if cidade.lower() in a["cidade"].lower()]
    return filtradas

@app.get("/acomodacoes/{id}")
def get_accommodations(id: int):
    try:
        cursor.execute("SELECT id, name, image, location, price FROM accommodations WHERE id = %s", (id,))
        accommodation = cursor.fetchone()

        if not accommodation:
            raise HTTPException(status_code=404, detail="Acomodação não encontrada")

        return {
            "id": accommodation[0],
            "name": accommodation[1],
            "image": accommodation[2],
            "location": accommodation[3],
            "price": accommodation[4]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar do banco: {str(e)}")

@app.post("/acomodacoes")
def create_accommodations(accommodation: Accommodation):
    print(accommodation)
    try:
        cursor.execute(
            "INSERT INTO accommodations (name, image, location, price) VALUES (%s, %s, %s, %s) RETURNING id",
            (accommodation.name, accommodation.image, accommodation.location, accommodation.price)
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        return {"mensagem": "Acomodação criada com sucesso", "id": new_id, "dados": accommodation}
    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao inserir no banco: {str(e)}")
# Etapa 1: Usar a imagem base do Python
FROM python:3.9-slim

# Etapa 2: Definir o diretório de trabalho dentro do container
WORKDIR /app

# Etapa 3: Copiar os arquivos do back-end para dentro do container
COPY . /app/

# Etapa 4: Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Expor a porta em que o FastAPI estará rodando
EXPOSE 8000

# Etapa 6: Comando para rodar o servidor FastAPI
CMD ["uvicorn", "api_acomodacao:app", "--host", "0.0.0.0", "--port", "8000"]

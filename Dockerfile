# Etapad 1: Imagem base para o build
FROM python:3.12 AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Carrega o arquivo de ambiente do python (libs e packages)
COPY requirements.txt /app/

# Instala as dependencias
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# Etapad 2: Imagem final
FROM python:3.12-slim AS final

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar libpq5 para suportar psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias ja instaladas do builder
COPY --from=builder /install /usr/local

# Copiar os arquivos do projeto
COPY . /app

# Criar script de entrypoint para executar migrate antes de iniciar

# Porta do projeto
EXPOSE 8000


# Dockerfile para PostgreSQL personalizado (opcional)
# Se não precisar de customizações, use a imagem oficial no docker-compose.yml

FROM postgres:18-alpine

RUN psql -U postgres -c "CREATE DATABASE db OWNER api;" 

# Variáveis de ambiente padrão
ENV POSTGRES_USER=api \
    POSTGRES_PASSWORD=${DB_PASSWORD} \
    POSTGRES_DB=db 
    

# Criar pasta para scripts de inicialização (se necessário)
RUN mkdir -p /docker-entrypoint-initdb.d

# Adicionar scripts customizados aqui se precisar
# COPY init-scripts/ /docker-entrypoint-initdb.d/


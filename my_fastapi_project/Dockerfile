# Utiliser l'image officielle PostgreSQL
FROM postgres:latest

# Copier le fichier d'initialisation dans le dossier approprié
COPY ../db/initialisation.sql /docker-entrypoint-initdb.d/

# Spécifier un utilisateur et mot de passe (optionnel si vous avez besoin de configurer la base de données initiale)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=Gu4de!oupe
ENV POSTGRES_DB=coord

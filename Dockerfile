# Utiliser une image Python comme base
FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Copier le fichier des dépendances Python
COPY requirements.txt /app/requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier le code de l'application
COPY . /app

# Définir le répertoire de travail
WORKDIR /app

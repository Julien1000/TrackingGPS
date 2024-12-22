# Utiliser une image Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers Python dans le conteneur
COPY . /app

RUN pip install --upgrade pip
# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt


# Commande par défaut pour exécuter le script en continu
CMD ["python", "producer.py"]

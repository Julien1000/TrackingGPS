# consumer/front/Dockerfile

FROM node:20-alpine

WORKDIR /app

# Copie des fichiers de package
COPY package*.json ./

# Installation des dépendances
RUN npm install

# Copie du reste du code
COPY . .

# Pour un mode dev avec hot reload (vite ou vue-cli)
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

## TODO Tester sur un nouveau projet si la map marche bien, la ya moy elle marche juste parce que c'est deja installé
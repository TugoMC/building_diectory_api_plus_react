# Utiliser une image Python officielle comme image de base
FROM python:3.12.6

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le répertoire de travail
COPY . /app

# Installer les dépendances du projet
RUN pip install -r requirements.txt

# Exposer le port sur lequel le serveur Django va écouter
EXPOSE 8000

# Lancer le serveur Django lorsque le conteneur démarre
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

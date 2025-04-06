FROM python:3.11-slim

WORKDIR /app

# Copie des fichiers de requirements
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le projet
COPY . .

# Lancement de l'app (adapte si ce n’est pas main.py)
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "main:server"]

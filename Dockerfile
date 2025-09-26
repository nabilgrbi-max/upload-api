# Étape 1: On part d'une base Linux avec Python
FROM python:3.13-slim

# Étape 2: On installe les outils système (dont RubberBand)
RUN apt-get update && apt-get install -y rubberband-cli

# Étape 3: On prépare le dossier de travail et on installe les paquets Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 4: On copie le reste de notre code
COPY . .

# Étape 5: On définit la commande pour démarrer le serveur
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "10000"]
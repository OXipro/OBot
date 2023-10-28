# Utilisez une image de base Python
FROM python:3.10-bullseye

# Copiez votre code Python dans le conteneur
COPY main.py /app/main.py
COPY rick.py /app/rick.py
COPY phrases.py /app/phrases.py
COPY requirements.txt /app/requirements.txt

RUN ls /app/


# Installez les dépendances Python si nécessaire
RUN pip install -r /app/requirements.txt
RUN apt update
RUN apt install -y ffmpeg 

# Définissez l'argument pour le token (le token par défaut est 'default_token')
ARG TOKEN=default_token

# Exécutez votre programme Python avec le token en tant qu'argument
# CMD ["python", "/app/main.py", "--token", "$TOKEN"]
CMD python /app/main.py --token ${TOKEN}
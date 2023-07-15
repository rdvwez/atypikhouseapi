FROM python:3.10

# On definit le dossier de travail
WORKDIR /app
RUN ls -l

#On compir le fichier requirements.txt dans le dossier de travail
COPY requirements.txt .

# Installez les dépendances dans un environnement virtuel
# RUN python3 -m venv venv
# RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# RUN python3 -m venv venv \
#     && pip3 install -U pip wheel\
#     && . /venv/bin/activate \
#     && pip install --no-cache-dir -r requirements.txt

# Créer et activer l'environnement virtuel
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

# Mettre à jour pip et installer wheel
RUN pip install --upgrade pip
RUN pip install wheel

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On execute le le fichier requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

#On copie le reste des fichiers du prjet
COPY . .
# On expose le port sur lequel l'application Flask sera accessible
EXPOSE 5000
 
# On Définit les variables d'environnement si nécessaire
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# On Commande pour exécuter l'application Flask
CMD ["python3", "app.py"]

# Fait exactement la même chose que la commande ci dessus
# ENTRYPOINT ["flask", "run"]

# CMD ["falsk", "run", "--host", "0.0.0.0"]
# CMD ["pyhton3", "run.PY"]
# CMD ["/bin/bash", "docker-entrypoint.sh"]
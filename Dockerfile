FROM pyhton:3.10

# EXPOSE 5000

#on se positionne dans app
WORKDIR /app

#on copie le requirements.txt dans le workdir
COPY requirements.txt .

#on execute le fichier requirements.txt pour installer tous les modules
# RUN pip install -r requiremants.txt
RUN pip install --no-cache-dir --upgrade -r requiremants.txt
 
#On copie le reste du l'application
COPY . .

# CMD ["falsk", "run", "--host", "0.0.0.0"]
# CMD ["pyhton3", "run.PY"]
CMD ["/bin/bash", "docker-entrypoint.sh"]
FROM pyhton:3.10

# EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

# RUN pip install -r requiremants.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
 
COPY . .

# CMD ["falsk", "run", "--host", "0.0.0.0"]
# CMD ["pyhton3", "run.PY"]
CMD ["/bin/bash", "docker-entrypoint.sh"]
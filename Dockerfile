# Usa un'immagine base di Python
FROM python:3.12

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copio il file requirements, va fatto anche se ho il volume
COPY /src/requirements.txt /app/requirements.txt
# Installa le dipendenze
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]

# Usa un'immagine base di Python
FROM python:3.12

# Imposta la directory di lavoro nel container
WORKDIR /app

# Installa le dipendenze
RUN pip install --no-cache-dir -r /app/requirements.txt


# Specifica il comando per eseguire l'applicazione
# Sostituisci `cli.py` con il nome del file che avvia la tua applicazione Flask
CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["tail","-f", "/dev/null"]

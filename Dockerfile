# Usa un'immagine base di Python
FROM python:3.12

# Imposta la directory di lavoro nel container
WORKDIR /app

#RUN git clone https://github.com/SamueleLonghin/generatore-tornei .

# Copio il file requirements, va fatto anche se ho il volume
COPY requirements.txt /app/

# Installa le dipendenze
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["flask", "run", "--host=0.0.0.0"]

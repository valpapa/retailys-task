FROM python:3.11-slim

# Nastavíme pracovní adresář uvnitř kontejneru
WORKDIR /app

# Zkopírujeme soubory requirements a nainstalujeme závislosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Zkopírujeme zbytek aplikace
COPY . .

# Nastavíme proměnnou pro Flask (není nutná, ale pomáhá)
ENV PYTHONUNBUFFERED=1

# Flask běží na portu 8000
EXPOSE 8000

# Spuštění aplikace (Flask server)
# ensure_xml() stáhne a rozbalí data ještě před startem serveru
CMD ["python", "-c", "from app import app; from functions import download_zip; download_zip(); app.run(host='0.0.0.0', port=8000)"]


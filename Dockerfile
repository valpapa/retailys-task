FROM python:3.12-slim

# Nepovinné, ale užitečné: žádné .pyc a UTF-8
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Zkopíruj soubory aplikace
COPY app.py functions.py . 

# Nainstaluj závislosti
RUN pip install --no-cache-dir flask requests

# Flask jede na 5000
EXPOSE 5000

# Spustí Flask server (viz if __name__ == "__main__" v app.py)
CMD ["python", "app.py", "runserver"]

FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (ADB)
RUN apt-get update && apt-get install -y android-tools-adb && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8722

CMD ["python", "main.py", "web"]
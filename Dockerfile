FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python files explicitly
COPY ["main.py", "server_config.py", "/app/"]

# Installa psutil per system stats
RUN pip install psutil

CMD ["python", "main.py"]

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_server.py .

# Installa psutil per system stats
RUN pip install psutil

CMD ["python", "mcp_server.py"]

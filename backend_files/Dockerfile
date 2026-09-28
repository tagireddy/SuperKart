FROM python:3.11-slim

WORKDIR /app

COPY backend_files/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend_files /app/backend_files

EXPOSE 7860

CMD ["python", "backend_files/app.py"]

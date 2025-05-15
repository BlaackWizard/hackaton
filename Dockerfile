# Используем официальный Python образ как базовый
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY backend /app/backend

ENV PYTHONPATH=/app

EXPOSE 8000

# Команда запуска приложения
CMD ["python3", "backend/src/bootstrap/entrypoint/fast_api.py"]

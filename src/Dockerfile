FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей для tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создание не-root пользователя
RUN useradd -m -u 1000 gameuser
USER gameuser

# Запуск игры
CMD ["python", "main.py"]
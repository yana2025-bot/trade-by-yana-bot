# Используем официальный Python образ
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запуск бота
CMD ["python", "main.py"]

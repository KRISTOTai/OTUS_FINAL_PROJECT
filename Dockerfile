FROM python:3.12-slim

# Установка curl и системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    wget \
    unzip \
    libnss3 \
    libxss1 \
    libgtk-3-0 \
    libasound2 \
    libgbm-dev \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Установка Brave
RUN curl -fsSL https://brave-browser-apt-release.s3.brave.com/brave-core.asc | gpg --dearmor -o /usr/share/keyrings/brave-browser-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" \
    > /etc/apt/sources.list.d/brave-browser-release.list && \
    apt-get update && apt-get install -y brave-browser

# Установка зависимостей проекта
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Создание рабочей директории
WORKDIR /app

# Копируем весь проект внутрь контейнера
COPY . /app

# Команда по умолчанию для запуска тестов
ENTRYPOINT ["pytest"]
CMD ["-v", "--alluredir=allure-results"]
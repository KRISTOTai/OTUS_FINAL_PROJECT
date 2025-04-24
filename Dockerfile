FROM python:3.12-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
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

# Установка Brave версии 135.0.7049.100
RUN wget -O /tmp/brave.zip https://github.com/brave/brave-browser/releases/download/v1.77.100/brave-browser-1.77.100-linux-amd64.zip&& \
    unzip /tmp/brave.zip -d /opt/brave && \
    ln -s /opt/brave/brave-browser /usr/bin/brave && \
    rm /tmp/brave.zip

# Установка Python зависимостей
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копирование проекта
WORKDIR /app
COPY . /app

ENTRYPOINT ["pytest"]
CMD ["-v", "--alluredir=allure-results"]
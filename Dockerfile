FROM python:3.12-slim

# Устанавливаем зависимости
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
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Brave
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    curl \
    && curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | tee /etc/apt/sources.list.d/brave-browser-release.list \
    && apt-get update \
    && apt-get install -y brave-browser=1.77.100 \
    && rm -rf /var/lib/apt/lists/*

# Создаем симлинк для Brave
RUN ln -s /usr/bin/brave-browser /usr/bin/brave

# Устанавливаем Python-зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем проект
WORKDIR /app
COPY . /app

CMD ["pytest", "-v", "--host=mariadb", "--url=http://opencart:8080", "--alluredir=allure-results", "--headless", "--browser=br", "--container"]
FROM python:3.9-slim

# 1. Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl ffmpeg xvfb xauth unzip \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
    libpangocairo-1.0-0 libgtk-3-0 libx11-xcb1 libxtst6 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Установка Allure CLI
RUN wget https://github.com/allure-framework/allure2/releases/download/2.20.1/allure-2.20.1.zip \
    && unzip allure-2.20.1.zip \
    && mv allure-2.20.1 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/bin/allure \
    && rm allure-2.20.1.zip

# 3. Устанавливаем переменные окружения для Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# 4. Создание рабочей директории
WORKDIR /app

# 5. Копируем requirements и устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Устанавливаем браузеры Playwright
RUN playwright install --with-deps

# 7. Копируем проект
COPY . /app

# 8. Создаем папку для allure-результатов, если ее нет
RUN mkdir -p /app/allure-results

# 9. Запускаем тесты через xvfb-run
CMD ["xvfb-run", "-a", "pytest", \
     "--alluredir=allure-results && cp /tmp/videos/*.webm /app/allure-result", \
     "--video=on", \
     "--tracing=retain-on-failure", \
     "--capture=tee-sys"]

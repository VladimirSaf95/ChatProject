FROM python:3.9.13-alpine3.16

# Обновляем репозитории APK
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# Устанавливаем необходимые пакеты
RUN apk update && \
    apk add --no-cache chromium chromium-chromedriver tzdata && \
    apk add openjdk11-jre curl tar && \
    apk add --no-cache wget

# Устанавливаем пакеты GLibC
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk && \
    apk add glibc-2.30-r0.apk glibc-bin-2.30-r0.apk

# Устанавливаем Allure
RUN curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz && \
    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm allure-2.13.8.tgz

# Устанавливаем рабочую директорию
WORKDIR /usr/workspace

# Копируем файл зависимостей в рабочую директорию
COPY ./requirements.txt /usr/workspace

# Устанавливаем зависимости Python
RUN pip3 install -r requirements.txt
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 复制wheel文件到/app目录下
COPY fief_server-0.28.6-py3-none-any.whl /app/

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/  && pip config set install.trusted-host mirrors.aliyun.com

RUN apt-get update && apt-get install -y build-essential redis libpq-dev \
    && pip install --upgrade pip supervisor \
    && python --version \
    && pip install fief_server-0.28.6-py3-none-any.whl \
    && apt-get autoremove -y build-essential \
    && mkdir -p /data/db

COPY supervisord.conf /etc/supervisord.conf

ENV DATABASE_LOCATION=/data/db
ENV SECRETS_DIR /run/secrets

ENV PORT=8000
EXPOSE ${PORT}

CMD ["supervisord", "-c", "/etc/supervisord.conf"]

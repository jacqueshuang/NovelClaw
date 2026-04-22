FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /app/requirements.txt

RUN python -m pip install -r /app/requirements.txt

COPY . /app/apps/auth-portal

RUN mkdir -p /app/apps/auth-portal/local_web_portal/data

WORKDIR /app/apps/auth-portal

EXPOSE 8010

CMD ["python", "-m", "uvicorn", "local_web_portal.app.main:app", "--host", "0.0.0.0", "--port", "8010"]

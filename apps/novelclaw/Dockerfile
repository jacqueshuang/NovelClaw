FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /app/requirements.base.txt
COPY local_web_portal/requirements.txt /app/requirements.web.txt

RUN pip install -r /app/requirements.base.txt -r /app/requirements.web.txt

COPY . /app/apps/novelclaw

RUN mkdir -p /app/apps/novelclaw/local_web_portal/data \
    /app/apps/novelclaw/local_web_portal/runs

WORKDIR /app/apps/novelclaw

EXPOSE 8012

CMD ["python", "-m", "uvicorn", "local_web_portal.app.main:app", "--host", "0.0.0.0", "--port", "8012"]

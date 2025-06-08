FROM python:3.10.9

ENV HOST=0.0.0.0:6798 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /rare-hashes-website

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY ./app ./app
COPY .env .
COPY ./ssl ./ssl

EXPOSE 6798

CMD ["hypercorn", "main:app", \
        "--bind", "0.0.0.0:6798", \
        "--certfile", "./ssl/rareHashes.crt", \
        "--keyfile", "./ssl/rareHashes.key"]
FROM python:3.10.9

WORKDIR /rare-hashes-website

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY ./app ./app
COPY .env .
COPY ./ssl ./ssl

CMD ["python", "./main.py"]
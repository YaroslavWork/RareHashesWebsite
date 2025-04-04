FROM python:3.13

WORKDIR /rare-hashes-website

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY database.py .
COPY functions.py .
COPY .env .
COPY ./static ./static
COPY ./templates ./templates
COPY ./ssl ./ssl

CMD ["python", "./main.py"]
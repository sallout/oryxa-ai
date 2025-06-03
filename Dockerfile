FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./model ./model
COPY ./prompt.txt .
COPY ./metadata.json .
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
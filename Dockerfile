FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /app

WORKDIR /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "src.flask_api"]

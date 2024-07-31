FROM python:3.10-slim

#set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#set woking directory
WORKDIR /app

COPY aws-cdk-flask/App/requirements.txt .

#RUN apk add build-base

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn  # as the app server

RUN python -m spacy download en_core_web_sm

COPY aws-cdk-flask/App .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "lambda_handler:app"]

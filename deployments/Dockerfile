FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /zadala

WORKDIR /zadala

COPY ../ .

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver"]

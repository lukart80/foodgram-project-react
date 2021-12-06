FROM python:3.8

WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 manage.py runserver 0:8000

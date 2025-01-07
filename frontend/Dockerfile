FROM python:latest

WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY program program/
RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app/program

CMD ["uvicorn", "views:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
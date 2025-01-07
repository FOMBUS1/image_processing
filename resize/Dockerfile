FROM python:latest

WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./resize.py /app/
RUN pip install -r requirements.txt

EXPOSE 8002

CMD ["uvicorn", "resize:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]
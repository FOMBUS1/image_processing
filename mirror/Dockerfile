FROM python:latest

WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./mirror.py .
RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "mirror:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
FROM python:3.10

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY ./main.py ./

EXPOSE 5000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
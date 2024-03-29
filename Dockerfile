FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
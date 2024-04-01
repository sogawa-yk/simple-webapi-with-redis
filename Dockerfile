# Pythonベースイメージの指定
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app
COPY cert.json .

WORKDIR /app/src

#CMD ["python", "src/query.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
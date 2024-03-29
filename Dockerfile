# Pythonベースイメージの指定
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# # Oracle Instant Clientのダウンロードとインストールに必要なパッケージのインストール
# RUN apt-get update && apt-get install -y libaio1 wget unzip \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Oracle Instant Clientのダウンロード先URL
# # Oracleのウェブサイトで最新バージョンのリンクを確認してください
# # ここでは例として19.3バージョンのBasic Light Packageを使用しています
# ENV CLIENT_URL=https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip

# # Oracle Instant Clientのダウンロードと解凍
# RUN wget -q ${CLIENT_URL} -O instantclient.zip \
#     && unzip instantclient.zip -d /opt/oracle \
#     && rm instantclient.zip \
#     && mv /opt/oracle/instantclient_* /opt/oracle/instantclient

# # Oracle Instant Clientのパスを環境変数に設定
# ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH
# ENV PATH=/opt/oracle/instantclient:$PATH

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app
COPY cert.json .

CMD ["python", "src/query.py"]
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
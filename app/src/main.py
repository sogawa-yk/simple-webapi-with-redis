from fastapi import FastAPI
from adb_client import AdbClient
from redis_client import RedisClient
from query import query_data, query_data_use_cache

app = FastAPI()
cert_path = "/app/cert.json"
adb_client = AdbClient(cert_path)
redis_client = RedisClient(cert_path)

@app.get("/db-columns-nocache")
async def get_db_columns_nocache():
    # キャッシュを利用しない場合
    sql_query = "SELECT * FROM PRODUCTS FETCH FIRST 100 ROWS ONLY"
    return query_data(adb_client, redis_client, sql_query)



@app.get("/db-columns-cache")
async def get_db_columns_cache():
    # キャッシュを利用する場合
    sql_query = "SELECT * FROM PRODUCTS FETCH FIRST 100 ROWS ONLY"
    return query_data_use_cache(adb_client, redis_client, sql_query)
from fastapi import FastAPI
from adb_client import AdbClient
from redis_client import RedisClient
from query import query_data, query_data_use_cache

app = FastAPI()
cert_path = "/app/cert.json"
adb_client = AdbClient(cert_path)
redis_client = RedisClient(cert_path)


@app.get("/all-data-nocache")
async def get_all_data_nocache():
    # キャッシュを利用しない場合
    sql_query = "SELECT * FROM PRODUCTS"
    return query_data(adb_client, redis_client, sql_query)


@app.get("/all-data-cache")
async def get_all_data_cache():
    # キャッシュを利用する場合
    sql_query = "SELECT * FROM PRODUCTS"
    return query_data_use_cache(adb_client, redis_client, sql_query)


@app.get("/conditional-data-nocache")
async def get_conditional_data_nocache():
    # キャッシュを利用する場合
    sql_query = "SELECT * FROM PRODUCTS WHERE PRODUCT_ID < 100"
    return query_data(adb_client, redis_client, sql_query)


@app.get("/conditional-data-cache")
async def get_conditional_data_cache():
    # キャッシュを利用する場合
    sql_query = "SELECT * FROM PRODUCTS WHERE PRODUCT_ID < 100"
    return query_data_use_cache(adb_client, redis_client, sql_query)


@app.get("/sorted-all-data-nocache")
async def get_sorted_all_data_nocache():
    # キャッシュを利用しない場合
    sql_query = "SELECT product_name, price, stock_quantity \
                FROM ( \
                SELECT product_name, price, stock_quantity \
                FROM products \
                ORDER BY price DESC, stock_quantity DESC \
                )"
    return query_data(adb_client, redis_client, sql_query)


@app.get("/sorted-all-data-cache")
async def get_sorted_all_data_cache():
    # キャッシュを利用する場合
    sql_query = "SELECT product_name, price, stock_quantity \
                FROM ( \
                SELECT product_name, price, stock_quantity \
                FROM products \
                ORDER BY price DESC, stock_quantity DESC \
                )"
    return query_data_use_cache(adb_client, redis_client, sql_query)


@app.get("/flushall")
async def flushall():
    return redis_client.flushall()



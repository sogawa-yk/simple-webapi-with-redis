import pandas as pd
from adb_client import AdbClient
from redis_client import RedisClient
import time

def query_data(adb_client, redis_client, sql):
  # Cacheにデータがあるかを確認
  cache_key = f"sql_cache:{sql}"
  cached_data = redis_client.get(cache_key)
  
  if cached_data is not None:
    # キャッシュからデータを取得
    cached_data_str = cached_data.decode('utf-8')
    return pd.read_json(cached_data_str)
  else:
    # Oracle Databaseからデータを取得
    df = adb_client.exec_sql(sql)
    
    # データをRedisにキャッシュする（例えば、10分間キャッシュする）
    redis_client.set(cache_key, 600, df.to_json(orient='records'))
    
    return df
  
def main():
  cert_path = "/app/cert.json"
  adb_client = AdbClient(cert_path)
  redis_client = RedisClient(cert_path)

  # キャッシュを利用しない場合
  redis_client.flushall()
  start_time = time.perf_counter()
  sql_query = "SELECT * FROM PRODUCTS"
  data = query_data(adb_client, redis_client, sql_query)
  end_time = time.perf_counter()
  elapsed_time = end_time - start_time
  print(f'キャッシュを利用しない場合に処理にかかった時間: {elapsed_time}秒')

  # キャッシュを利用する場合
  start_time = time.perf_counter()
  sql_query = "SELECT * FROM PRODUCTS"
  data = query_data(adb_client, redis_client, sql_query)
  end_time = time.perf_counter()
  elapsed_time = end_time - start_time
  print(f'キャッシュを利用する場合に処理にかかった時間: {elapsed_time}秒')

if __name__ == '__main__':
  main()
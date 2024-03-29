import pandas as pd
from adb_client import AdbClient
from redis_client import RedisClient

def query_data(adb_client, redis_client, sql):
  # Cacheにデータがあるかを確認
  cache_key = f"sql_cache:{sql}"
  cached_data = redis_client.get(cache_key)
  
  if cached_data is not None:
    # キャッシュからデータを取得
    return pd.read_json(cached_data)
  else:
    # Oracle Databaseからデータを取得
    df = adb_client.exec_sql(sql)
    
    # データをRedisにキャッシュする（例えば、10分間キャッシュする）
    redis_client.setex(cache_key, 600, df.to_json())
    
    return df
  
def main():
  cert_path = "/app/cert.json"
  adb_client = AdbClient(cert_path)
  redis_client = RedisClient(cert_path)

  # データクエリの例
  sql_query = "SELECT * FROM PRODUCTS"
  data = query_data(adb_client, redis_client, sql_query)
  print(data)

if __name__ == '__main__':
  main()
import pandas as pd
from adb_client import AdbClient
from redis_client import RedisClient

def query_data_use_cache(adb_client, redis_client, sql):
  # Cacheにデータがあるかを確認
  cache_key = f"sql_cache:{sql}"
  cached_data = redis_client.get(cache_key)
  
  if cached_data is not None:
    # キャッシュからデータを取得
    cached_data_str = cached_data.decode('utf-8')
    return cached_data_str#pd.read_json(cached_data_strz)
  else:
    # Oracle Databaseからデータを取得
    df = adb_client.exec_sql(sql)
    
    # データをRedisにキャッシュする（例えば、10分間キャッシュする）
    redis_client.set(cache_key, 600, df.to_json(orient='records'))
    
    return df.to_json()

def query_data(adb_client, redis_client, sql):
  # Oracle Databaseからデータを取得
  df = adb_client.exec_sql(sql)

  return df.to_json()
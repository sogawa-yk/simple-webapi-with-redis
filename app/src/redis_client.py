## Redisとの接続
import redis
import json

class RedisClient():
  def __init__(self, cert_path):
    with open(cert_path, 'r') as f:
      redis_cert_info = json.load(f)['redis']

    self.connection = redis.Redis(host=redis_cert_info['host'], port=6379, db=0, ssl=True)

  def get(self, key):
    return self.connection.get(key)

  def setex(self, key, value, ttl):
    return self.connection.setex(key, ttl, value)
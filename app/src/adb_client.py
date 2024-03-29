## Oracle Databaseとの接続
import oracledb
import pandas as pd
import json

class AdbClient():
  def __init__(self, cert_path):
    with open(cert_path, 'r')as f:
      db_cert_info = json.load(f)['oracle_database']
    
    self.connection = oracledb.connect(user=db_cert_info['user'], password=db_cert_info['password'], dsn=db_cert_info['con_str'])

  def exec_sql(self, sql):
    return pd.read_sql(sql, self.connection)
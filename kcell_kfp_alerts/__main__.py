import findspark
findspark.init('/opt/spark3')

import time
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
import logging
logging.basicConfig(format="%(asctime)s %(message)s")
logging.getLogger().setLevel(logging.INFO)

spark_config = {"spark.dynamicAllocation.maxExecutors": "30","spark.dynamicAllocation.minExecutors": "1","spark.dynamicAllocation.initialExecutors": "1","spark.executor.cores": "1","spark.executor.memory": "4g","spark.driver.memory": "2g", "spark.eventLog.enabled": "false"}
config = [(key, value) for key, value in spark_config.items()]
sconf = SparkConf().setAppName('oracle_import').setAll(config)

spark = SparkSession.builder.config(conf=sconf).enableHiveSupport().getOrCreate()

oracle_user = ""
oracle_password = ""

with open('/etc/oracle-secret/username', 'r') as file:
  oracle_user = file.read()

with open('/etc/oracle-secret/password', 'r') as file:
  oracle_password = file.read()


def get_spark(query, options):
  return (spark.read
          .format("jdbc")
          .option("url", "jdbc:oracle:thin:@acrm-pmy.kcell.kz:1521/acrm")
          .option("user", oracle_user)
          .option("password", oracle_password)
          .option("dbtable", f'({query}) qry')
          .options(**options))

def get_result_safely(result, name):
  return result.collect()[0][name] if (result and result.collect()) else 0

def sensor():
    query = "select CASE WHEN MAX(a.log_time) IS NULL THEN 0 ELSE 1 END as CNT_ALL from dwh_adm.dwh_adm_log a where a.log_time >= trunc(sysdate) and a.module in ('PKG_OG_USAGE') and a.sub_module = 'insert_call_fact' and a.msg = 'Procedure finished'"
    options = {"fetchsize": "5"}
    # while (True):
    result = get_spark(query,options).load()
    cnt_all = get_result_safely(result, "CNT_ALL")
    if cnt_all < 3000000:
      logging.info(f"\n\n <<<<< The condition \n {query} \n has not been met! >>>>>")
      exit(1)
    # else:
    #     pass
    # logging.info("\n")
    # logging.info("The conditions has not been met")

    # time.sleep(60 * 10)

sensor()

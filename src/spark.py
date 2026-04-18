from pyspark.sql import SparkSession

class Spark:

    def __init__(self, app_name="Youtube_ETL"):
        self.app_name = app_name
        self.spark = self._create_spark_session()
    
    def _create_spark_session(self):
        spark = (
            SparkSession.builder.
            appName(self.app_name).
            getOrCreate()
        )
        return spark
    
    def get_session(self):
        return self.spark
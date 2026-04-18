from pyspark.sql import SparkSession

class Spark:

    def __init__(self, app_name="Youtube_ETL"):
        self.app_name = app_name
        self.spark = self._create_spark_session()
    
    def _create_spark_session(self):
        spark = (
            SparkSession.builder
            .appName(self.app_name)
            .config("spark.jars.packages", "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.6")
            .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
            .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
            .getOrCreate()
        )
        return spark
    
    def get_session(self):
        return self.spark
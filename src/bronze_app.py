from pyspark.sql.functions import col, current_date, lit, year, month, dayofmonth
from spark import Spark
from bucket import Bucket
import logging

class BronzeToSilver:

    def __init(self, project_id, env_sufix):

        self.spark_manager = Spark(app_name="Youtube_Bronze_to_Silver")
        self.spark = self.spark_manager.get_session()

        self.bucket_manager = Bucket(self.spark)

        self.bronze_bucket = f"gs://youtube-etl{env_sufix}-bronze-lake/"
        self.silver_bucket = f"gs://youtube-etl{env_sufix}-silver-lake/"


    def process_global_data(self):

        logging.info("Iniciando processamento dos dados Globais")

        input_path = f"gs://{self.bronze_bucket}/raw/global_top4k.csv"

        df_raw = self.bucket_manager.read_bucket(
            bucket_name=self.bronze_bucket,
            path=input_path,
            format="csv",
            header=True,
            infer_schema=True            
        )

        logging.info("Aplicando transformações e padronizando colunas")

        df_clean = df_raw.withColumnRenamed("Global Rank", "global_rank")\
                        .withColumnRenamed("Channel ID", "channel_id")\
                        .withColumnRenamed("Channel Name", "channel_name")\
                        .withColumnRenamed("Subscribers", "subscribers")\
                        .withColumnRenamed("Total Views", "total_views")\
                        .withColumnRenamed("Total Videos", "total_videos")\
                        .withColumnRenamed("Country", "country")\
                        .withColumnRenamed("Description", "description")
        
        df_final = df_clean.withColumn("ingestion_date", current_date())\

        df_final = df_final.withColumn("year", year(col("ingestion_date"))) \
                           .withColumn("month", month(col("ingestion_date"))) \
                           .withColumn("day", dayofmonth(col("ingestion_date")))
        
        dados_str = df_final._jdf.showString(5, 20, False)
        logging.info(f"Visualização dos dados (Top 5):\n{dados_str}")

        schema_str = df_final._jdf.schema().treeString()
        logging.info(f"Visualização do schema dos dados:\n{schema_str}")

        outputh_path = f"gs://{self.silver_bucket}/global_channels/"

        self.bucket_manager.write_bucket(
            df= df_final,
            path=outputh_path,
            format="parquet",
            mode="append",
            partition_cols=["year", "month", "day"]
        )

        logging.info("Processamento dos dados Globais concluído com sucesso!")




            

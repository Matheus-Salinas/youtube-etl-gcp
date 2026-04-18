from pyspark.sql.functions import col, current_date, lit, year, month, dayofmonth
from spark import Spark
from bucket import Bucket
from datetime import datetime
import logging

class BronzeToSilver:

    def __init__(self, project_id, env_suffix):

        self.spark_manager = Spark(app_name="Youtube_Bronze_to_Silver")
        self.spark = self.spark_manager.get_session()

        self.bucket_manager = Bucket(self.spark)

        self.bronze_bucket = f"youtube-etl-gcp{env_suffix}_bronze_lake/"
        self.silver_bucket = f"youtube-etl-gcp{env_suffix}_silver_lake/"


    def process_global_data(self):

        print("Iniciando processamento dos dados Globais")

        input_path = f"gs://{self.bronze_bucket}/raw/global_top4k.csv"

        df_raw = self.bucket_manager.read_bucket(
            bucket_name=self.bronze_bucket,
            path=input_path,
            format="csv",
            header=True,
            infer_schema=True            
        )

        print("Aplicando transformações e padronizando colunas")

        df_clean = df_raw.withColumnRenamed("Global Rank", "global_rank")\
                        .withColumnRenamed("Channel ID", "channel_id")\
                        .withColumnRenamed("Channel Name", "channel_name")\
                        .withColumnRenamed("Subscribers", "subscribers")\
                        .withColumnRenamed("Total Views", "total_views")\
                        .withColumnRenamed("Total Videos", "total_videos")\
                        .withColumnRenamed("Country", "country")\
                        .withColumnRenamed("Description", "description")
        
        df_final = df_clean.withColumn("ingestion_date", current_date())\

        dados_str = df_final._jdf.showString(5, 20, False)
        print(f"Visualização dos dados (Top 5):\n{dados_str}")

        schema_str = df_final._jdf.schema().treeString()
        print(f"Visualização do schema dos dados:\n{schema_str}")

        now = datetime.now()

        year = now.strftime("%y")
        month = now.strftime("%m")
        day = now.strftime("%Y%m%d")

        output_path = f"gs://{self.silver_bucket}/global_channels/Year/{year}/Month/{month}/{day}/"

        self.bucket_manager.write_bucket(
            df= df_final,
            path=output_path,
            format="parquet",
            mode="overwrite",
        )

        print("Processamento dos dados Globais concluído com sucesso!")

if __name__ == "__main__":
    etl = BronzeToSilver(project_id="youtube-etl-gcp-493418", env_suffix="-dev")
    etl.process_global_data()




            

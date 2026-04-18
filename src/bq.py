import logging

class Bigquery:

    def __init__(self, spark_session, temp_gcs_bucket):

        self.spark = spark_session
        self.temp_gcs_bucket = temp_gcs_bucket
        
        self.spark.config.set("viewEnabled", "true")
        self.spark.config.set("materializationDataset", "temp_dataset")

    def write_to_bq(self, df, table_id, mode):
        logging.info(f"Enviando dados para a tabela BigQuery: {table_id} no modo {mode}")

        df.write.format("bigquery")\
            .option("temporaryGcsBucket", self.temp_gcs_bucket)\
            .option("table", table_id)\
            .mode(mode)\
            .save()
        
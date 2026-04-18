import logging

class Bucket:

    def __init__(self, spark_session):
        self.spark = spark_session

    def read_bucket(self, bucket_name,path, format, header=True, infer_schema=True):
        print(f"Lendo arquivos do Bucket: {bucket_name}. No caminho :{path}")
        df = self.spark.read.format(format)\
            .option("header", header)\
            .option("inferSchema", infer_schema)\
            .load(path)
        return df
    
    def write_bucket(self, df, path, format, mode, partition_cols=None):
        print(f"Escrevendo dados em formato {format}. No caminho :{path}")
        
        writer = df.write.format(format).mode(mode)

        if partition_cols:
            print(f"Particionando pelos campos: {partition_cols}")
            writer = writer.partitionBy(*partition_cols)

        writer.save(path)
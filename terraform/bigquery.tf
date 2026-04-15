resource "google_bigquery_dataset" "gold_lake"{
    project = var.project_id
    dataset_id = "${local.bq_prefix}_gold"
    description = "Camada Gold com dados limpos e agregados."
    location = var.region
}

resource "google_bigquery_table" "tb_youtube_gold" {
  project = var.project_id
  dataset_id = google_bigquery_dataset.gold_lake.dataset_id
  table_id = "tb_youtube_channels_gold"
  description = "Tabela camada gold com dados pronto para consumo de analytics"
  schema = file("bigquery/schemas/tb_youtube_channels_gold.json")
  deletion_protection = false
  time_partitioning {
    type = "DAY"
    field = "ingestion_date"
  }
  clustering = ["country_code", "channel_id"]
}

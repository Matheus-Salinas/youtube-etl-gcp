resource "google_storage_bucket_iam_member" "bronze_acess" {
    bucket = google_storage_bucket.bronze_lake.name
    role = "roles/storage.admin"
    member = "serviceAccount:${google_service_account.etl_service_account.email}"
}

resource "google_storage_bucket_iam_member" "silver_acess" {
    bucket = google_storage_bucket.silver_lake.name
    role = "roles/storage.admin"
    member = "serviceAccount:${google_service_account.etl_service_account.email}"
}

resource "google_bigquery_dataset_iam_member" "gold_acess" {
    dataset_id = google_bigquery_dataset.gold_lake.dataset_id
    role = "roles/bigquery.dataEditor"
    member = "serviceAccount:${google_service_account.etl_service_account.email}"
    depends_on = [ google_bigquery_dataset.gold_lake ]
}
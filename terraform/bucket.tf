resource "google_storage_bucket" "bronze_lake" {
    name = "${local.gcs_prefix}_bronze_lake" 
    location = var.region
    force_destroy = true
    uniform_bucket_level_access = true
}

resource "google_storage_bucket" "silver_lake" {
    name = "${local.gcs_prefix}_silver_lake" 
    location = var.region
    force_destroy = true
    uniform_bucket_level_access = true
}


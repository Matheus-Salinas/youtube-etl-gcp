
terraform {
  backend "gcs" {
    bucket  = "youtube-etl-gcp-terraform-state"
    prefix  = "terraform/state"
  }
}
provider "google" {
    project = var.project_id
    region = var.region
}
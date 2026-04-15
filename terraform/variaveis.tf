variable "project_id" {
    description = "Identificador do meu projeto GCP"
    type = "String"
}

variable "region" {
    description = "Região para projeto GCP"
    type = "String"
    default = "us-central1"
}

variable "repo_name" {
    description = "Nome do repositorio no GitHub (ex: youtube-etl)"
    type = "Stringt"
}

variable "branch" {
    description = "Nome da branch atual do GitHub (ex: dev, feature-1)"
    type = "String"
    default = "dev"
}


locals {
  env_suffix = var.branch == "main" ? "" : "-${var.branch}"
  
  gcs_prefix = "${var.repo_name}${local.env_suffix}"

  bq_env_suffix = var.branch == "main" ? "" : "_${var.branch}"
  bq_prefix     = "${replace(var.repo_name, "-", "_")}${local.bq_env_suffix}"
}
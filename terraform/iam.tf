resource "google_service_account" "etl_service_account"{
    account_id = "sa-${replace(var.repo_name, "-", "")}${local.env_suffix}"
    display_name = "Conta de serviço para ETL dos dados Youtube"
    description = "Usada pelos scripts em PySpark para acessar os Buckets e BigQuery"
}
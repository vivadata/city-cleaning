resource "google_storage_bucket" "cc_storage_bucket" {
  name     = "cc-datasets-storage-${terraform.workspace}"
  location = "EU"
}

resource "google_bigquery_dataset" "cc_bigquery_dataset" {
  dataset_id = "city_cleaning_${terraform.workspace}"
}
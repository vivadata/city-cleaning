resource "google_project_service" "composer_api" {
  project                               = var.project_id
  service                               = "composer.googleapis.com"
  disable_on_destroy                    = false
#   check_if_service_has_usage_on_destroy = true
}

resource "google_service_account" "airflow_service_account" {
  account_id   = "airflow-service-account-${terraform.workspace}"
  display_name = "Example Custom Service Account"
}

resource "google_project_iam_member" "airflow_service_account" {
  project  = var.project_id
  member   = format("serviceAccount:%s", google_service_account.airflow_service_account.email)
  // Role for Public IP environments
  role     = "roles/composer.worker"
}

# Workaround: wait form iam to be propagated
resource "time_sleep" "wait_30_seconds" {
  depends_on = [google_service_account.airflow_service_account, google_project_iam_member.airflow_service_account]

  create_duration = "30s"
}

resource "google_composer_environment" "airflow_environment" {
  name = "city-cleaning-${terraform.workspace}"

  config {
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    software_config {
      image_version = "composer-3-airflow-2.10.5-build.14"
    }

    node_config {
      service_account = google_service_account.airflow_service_account.email
    }
  }

  storage_config {
    bucket = "city-cleaning-airflow-${terraform.workspace}"
  }

  depends_on = [ time_sleep.wait_30_seconds ]
}

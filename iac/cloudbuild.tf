resource "google_project_service" "cloudbuild_api" {
  project                               = var.project_id
  service                               = "cloudbuild.googleapis.com"
  disable_on_destroy                    = false
#   check_if_service_has_usage_on_destroy = true
}

resource "google_project_service" "secretmanager_api" {
  project                               = var.project_id
  service                               = "secretmanager.googleapis.com"
  disable_on_destroy                    = false
#   check_if_service_has_usage_on_destroy = true
}
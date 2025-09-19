terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
        version = "7.3.0"
    }
  }

  backend "gcs" {
    bucket = "rdp-tf-state"
  }
}

provider "google" {
  project = var.project_id
  region = var.region
}
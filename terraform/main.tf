terraform {
  required_version = "1.4.5"
  required_providers { aws = { version = "5.1.0" } }
  backend "s3" {
    bucket               = "diegor-terraform"
    workspace_key_prefix = ""
    key                  = "orcamento/terraform.tfstate"
    region               = "us-east-1"
    profile              = "diego"
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags { tags = local.provider_tags }
}

provider "google" {
  project = local.gcp_project
  region  = local.gcp_region
}

provider "google-beta" {
  project = local.gcp_project
  region  = local.gcp_region
}

provider "kubernetes" {
  host  = "https://${data.google_container_cluster.k8s.endpoint}"
  token = data.google_client_config.provider.access_token
  cluster_ca_certificate = base64decode(
    data.google_container_cluster.k8s.master_auth[0].cluster_ca_certificate,
  )
}

data "aws_caller_identity" "current" {}

data "google_client_config" "provider" {}

data "google_container_cluster" "k8s" {
  name     = "k8s"
  location = local.gcp_region
}

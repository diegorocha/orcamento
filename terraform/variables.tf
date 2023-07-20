locals {
  domain_name     = "diegorocha.com.br"
  subdomain       = "orcamento.${local.domain_name}"
  static_domain   = "orcamento-static.${local.domain_name}"
  contas_domain   = "orcamento-contas.${local.domain_name}"
  dns_destination = "k8s.${local.domain_name}"
  gcp_project     = "diegor-infra"
  gcp_region      = "us-central1"
  provider_tags = {
    service = "orcamento"
    backup  = "false"
  }
}
variable "app_image" {
  type    = string
  default = "us.gcr.io/diegor-infra/orcamento"
}

variable "app_version" {
  type = string
}

variable "orcamento_secrets" {
  type      = map(any)
  sensitive = true
}

output "orcamento_bucket_name" {
  value = aws_s3_bucket.static.bucket
}

output "ecr_repository_url" {
  value = aws_ecr_repository.ecr_repository.repository_url
}

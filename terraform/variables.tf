locals {
  domain_name     = "diegorocha.com.br"
  subdomain       = "orcamento.${local.domain_name}"
  static_domain   = "orcamento-static.${local.domain_name}"
  contas_domain   = "orcamento-contas.${local.domain_name}"
  dns_destination = "hardin.${local.domain_name}"
  provider_tags = {
    service = "orcamento"
    backup  = "false"
  }
}

output "orcamento_bucket_name" {
  value = aws_s3_bucket.static.bucket
}

output "orcamento_policies_arn" {
  value = [
    aws_iam_policy.policy_orcamento_s3.arn
  ]
}

output "ecr_repository_url" {
  value = aws_ecr_repository.ecr_repository.repository_url
}

locals {
  gcp_managed_zone = replace(local.domain_name, ".", "-")
}

resource "google_dns_record_set" "orcamento" {
  name = "${local.subdomain}."
  type = "CNAME"
  ttl  = 600

  managed_zone = local.gcp_managed_zone

  rrdatas = ["${local.dns_destination}."]
}

resource "google_dns_record_set" "contas" {
  name = "${local.contas_domain}."
  type = "CNAME"
  ttl  = 600

  managed_zone = local.gcp_managed_zone

  rrdatas = ["${aws_cloudfront_distribution.contas.domain_name}."]
}

resource "google_dns_record_set" "static" {
  name = "${local.static_domain}."
  type = "CNAME"
  ttl  = 600

  managed_zone = local.gcp_managed_zone

  rrdatas = ["${aws_cloudfront_distribution.static.domain_name}."]
}

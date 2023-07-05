/* Remove after migration of dns zone */
data "aws_route53_zone" "hosted_zone" {
  name = local.domain_name
}

locals {
  alias_records = ["A", "AAAA"]
}

resource "aws_route53_record" "record_orcamento" {
  zone_id = data.aws_route53_zone.hosted_zone.id
  name    = local.subdomain
  type    = "CNAME"
  ttl     = 60
  records = [local.dns_destination]
}

resource "aws_route53_record" "contas" {
  for_each = toset(local.alias_records)

  zone_id = data.aws_route53_zone.hosted_zone.zone_id
  name    = local.contas_domain
  type    = each.value
  alias {
    name                   = aws_cloudfront_distribution.contas.domain_name
    zone_id                = aws_cloudfront_distribution.contas.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "static" {
  for_each = toset(local.alias_records)

  zone_id = data.aws_route53_zone.hosted_zone.zone_id
  name    = local.static_domain
  type    = each.value
  alias {
    name                   = aws_cloudfront_distribution.static.domain_name
    zone_id                = aws_cloudfront_distribution.static.hosted_zone_id
    evaluate_target_health = false
  }
}
/* end-remove */

locals {
  gcp_managed_zone = replace(local.domain_name, ".", "-")
}

resource "google_dns_record_set" "orcamento" {
  name = "${local.subdomain}."
  type = "CNAME"
  ttl = 600

  managed_zone = local.gcp_managed_zone

  rrdatas = ["${local.dns_destination}."]
}

resource "google_dns_record_set" "contas" {
  name = "${local.contas_domain}."
  type = "CNAME"
  ttl = 600

  managed_zone = local.gcp_managed_zone

  rrdatas = ["${aws_cloudfront_distribution.contas.domain_name}."]
}

resource "google_dns_record_set" "static" {
  name = "${local.static_domain}."
  type = "CNAME"
  ttl = 600

  managed_zone = local.gcp_managed_zone

  rrdatas = ["${aws_cloudfront_distribution.static.domain_name}."]
}

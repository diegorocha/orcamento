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

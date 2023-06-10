data "aws_acm_certificate" "wildcard" {
  domain      = local.domain_name
  most_recent = true
}

resource "aws_cloudfront_origin_access_control" "contas" {
  name                              = aws_s3_bucket.contas.bucket
  description                       = "${aws_s3_bucket.contas.bucket} Policy"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "contas" {
  origin {
    origin_access_control_id = aws_cloudfront_origin_access_control.contas.id
    domain_name              = aws_s3_bucket.contas.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.contas.bucket
  }
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Distribution for ${local.contas_domain}"
  default_root_object = "index.html"

  aliases = [
    local.contas_domain
  ]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.contas.bucket

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    min_ttl                = 0
    default_ttl            = 300
    max_ttl                = 600
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = data.aws_acm_certificate.wildcard.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2019"
  }
}

resource "aws_cloudfront_origin_access_control" "static" {
  name                              = aws_s3_bucket.static.bucket
  description                       = "${aws_s3_bucket.static.bucket} Policy"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "static" {
  origin {
    origin_access_control_id = aws_cloudfront_origin_access_control.static.id
    domain_name              = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.static.bucket
  }
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Distribution for ${local.static_domain}"
  default_root_object = "index.html"

  aliases = [
    local.static_domain
  ]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.static.bucket

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    min_ttl                = 0
    default_ttl            = 300
    max_ttl                = 600
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = data.aws_acm_certificate.wildcard.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2019"
  }
}

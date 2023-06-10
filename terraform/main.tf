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

data "aws_caller_identity" "current" {}

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

resource "aws_s3_bucket" "static" {
  bucket = "orcamento-static"
}

resource "aws_s3_bucket_ownership_controls" "static" {
  bucket = aws_s3_bucket.static.bucket

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "static" {
  bucket = aws_s3_bucket.static.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "bucket_staticfiles_policy" {
  bucket = aws_s3_bucket.static.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowAllToRootAndCreator",
        Effect = "Allow",
        Principal = {
          "AWS" : [
            "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
            data.aws_caller_identity.current.arn,
          ]
        }
        Action = "s3:*",
        Resource = [
          aws_s3_bucket.static.arn,
          "${aws_s3_bucket.static.arn}/*",
        ]
      },
      {
        Sid    = "AllowCloudFrontServicePrincipalReadOnly",
        Effect = "Allow",
        Principal = {
          Service = "cloudfront.amazonaws.com"
        },
        Action   = "s3:GetObject",
        Resource = "${aws_s3_bucket.static.arn}/*",
        Condition = {
          "StringEquals" : {
            "AWS:SourceArn" : aws_cloudfront_distribution.static.arn,
          }
        }
      },
    ]
  })
}

resource "aws_iam_policy" "policy_orcamento_s3" {
  name        = "policy_orcamento_s3"
  path        = "/"
  description = "Policy to allow read/write to ${aws_s3_bucket.static.bucket} bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObjectAcl",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ]
        Resource = [
          aws_s3_bucket.static.arn,
          "${aws_s3_bucket.static.arn}/*",
          aws_s3_bucket.contas.arn,
          "${aws_s3_bucket.contas.arn}/*",
        ]
      },
    ]
  })
}

resource "aws_s3_bucket" "contas" {
  bucket = "orcamento-contas"
}

resource "aws_s3_bucket_ownership_controls" "contas" {
  bucket = aws_s3_bucket.contas.bucket

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "contas" {
  bucket = aws_s3_bucket.contas.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "bucket_contas_policy" {
  bucket = aws_s3_bucket.contas.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowAllToRootAndCreator",
        Effect = "Allow",
        Principal = {
          "AWS" : [
            "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
            data.aws_caller_identity.current.arn,
          ]
        }
        Action = "s3:*",
        Resource = [
          aws_s3_bucket.contas.arn,
          "${aws_s3_bucket.contas.arn}/*",
        ]
      },
      {
        Sid    = "AllowCloudFrontServicePrincipalReadOnly",
        Effect = "Allow",
        Principal = {
          Service = "cloudfront.amazonaws.com"
        },
        Action   = "s3:GetObject",
        Resource = "${aws_s3_bucket.contas.arn}/*",
        Condition = {
          "StringEquals" : {
            "AWS:SourceArn" : aws_cloudfront_distribution.contas.arn,
          }
        }
      },
    ]
  })
}

data "aws_route53_zone" "hosted_zone" {
  name = local.domain_name
}

resource "aws_route53_record" "record_orcamento" {
  zone_id = data.aws_route53_zone.hosted_zone.id
  name    = local.subdomain
  type    = "CNAME"
  ttl     = 60
  records = [local.dns_destination]
}

resource "aws_ecr_repository" "ecr_repository" {
  name                 = "orcamento"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    service = "orcamento"
  }
}

resource "aws_ecr_lifecycle_policy" "ecr_repository_lifecycle" {
  repository = aws_ecr_repository.ecr_repository.name

  policy = jsonencode(
    {
      rules = [
        {
          action = {
            type = "expire"
          }
          description  = "Keep last 3 images"
          rulePriority = 1
          selection = {
            countNumber = 3
            countType   = "imageCountMoreThan"
            tagStatus   = "any"
          }
        },
      ]
    }
  )
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

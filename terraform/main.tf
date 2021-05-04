terraform {
  required_version = "~>0.13"
  backend "s3" {
    bucket               = "diegor-terraform"
    workspace_key_prefix = ""
    key                  = "orcamento/terraform.tfstate"
    region               = "us-east-1"
    profile              = "diego"
  }
}

locals {
  domain_name = "diegorocha.com.br"
  subdomain = "orcamento.${local.domain_name}"
  dns_destination = "palver.${local.domain_name}"
}

resource "aws_s3_bucket" "bucket_staticfiles" {
  bucket = "orcamento-static"
  acl    = "private"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = [
      "https://orcamento.diegorocha.com.br",
      "http://localhost:8000"
    ]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  tags = {
    service = "orcamento"
    backup  = "false"
  }
}

resource "aws_s3_bucket_policy" "bucket_staticfiles_policy" {
  bucket = aws_s3_bucket.bucket_staticfiles.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action = [
          "s3:GetObject",
        ]
        Resource = [
          "${aws_s3_bucket.bucket_staticfiles.arn}/*"
        ]
      },
    ]
  })
}

resource "aws_iam_policy" "policy_orcamento_s3" {
  name        = "policy_orcamento_s3"
  path        = "/"
  description = "Policy to allow read/write to ${aws_s3_bucket.bucket_staticfiles.bucket} bucket"

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
          aws_s3_bucket.bucket_staticfiles.arn,
          "${aws_s3_bucket.bucket_staticfiles.arn}/*",
          aws_s3_bucket.bucket_contas.arn,
          "${aws_s3_bucket.bucket_contas.arn}/*",
        ]
      },
    ]
  })
}

resource "aws_s3_bucket" "bucket_contas" {
  bucket = "orcamento-contas"
  acl = "private"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = [
      "https://orcamento.diegorocha.com.br",
      "http://localhost:8000"
    ]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags = {
    service = "orcamento"
    backup  = "false"
  }
}

resource "aws_s3_bucket_policy" "bucket_contas_policy" {
  bucket = aws_s3_bucket.bucket_contas.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action = [
          "s3:GetObject",
        ]
        Resource = [
          "${aws_s3_bucket.bucket_contas.arn}/*"
        ]
      },
    ]
  })
}

data "aws_route53_zone" "hosted_zone" {
  name  = local.domain_name
}

resource "aws_route53_record" "record_orcamento" {
  zone_id = data.aws_route53_zone.hosted_zone.id
  name = local.subdomain
  type = "CNAME"
  ttl = 60
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
  value = aws_s3_bucket.bucket_staticfiles.bucket
}

output "orcamento_policies_arn" {
  value = [
    aws_iam_policy.policy_orcamento_s3.arn
  ]
}

output "contas_url" {
  value = aws_s3_bucket.bucket_contas.website_endpoint
}

output "ecr_repository_url" {
  value = aws_ecr_repository.ecr_repository.repository_url
}

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

resource "aws_iam_policy" "policy_orcamento_s3" {
  name        = "policy_orcamento_s3"
  path        = "/"
  description = "Policy to allow read/write on orcamento buckets"

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

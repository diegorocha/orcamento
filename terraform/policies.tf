locals {
  attach_policies_on_ec2_role       = true
  attach_policies_on_ec2_role_count = local.attach_policies_on_ec2_role ? 1 : 0
}


data "terraform_remote_state" "infra" {
  count = local.attach_policies_on_ec2_role_count

  backend = "s3"

  config = {
    bucket               = "diegor-terraform"
    workspace_key_prefix = ""
    key                  = "diegor-infra/terraform.tfstate"
    region               = "us-east-1"
    profile              = "diego"
  }
}

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

resource "aws_iam_role_policy_attachment" "ec2_role_policies_orcamento" {
  count      = local.attach_policies_on_ec2_role_count
  role       = data.terraform_remote_state.infra[count.index].outputs.roles.ec2
  policy_arn = aws_iam_policy.policy_orcamento_s3.arn
}

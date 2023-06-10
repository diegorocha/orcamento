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

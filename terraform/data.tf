# Fetch public subnets based on them being tagged as "public"
data "aws_subnets" "public_subnets" {
  filter {
    name   = "tag:Name"
    values = ["public-subnet-*"]
  }
}

output "aws_subnets" {
  value = data.aws_subnets.public_subnets.ids
}

data "aws_iam_policy_document" "ecs_assume_role" {
  statement {
    effect = "Allow"
    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }
    actions = ["sts:AssumeRole"]
  }
}
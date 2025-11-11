resource "aws_iam_role" "task_execution_role" {
  name               = "${var.ecs_cluster}-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume_role.json

  tags = merge(local.default_tags, {
    Name = "${var.ecs_cluster}-task-role"
  })
}

resource "aws_iam_role_policy_attachment" "task_execution_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  role       = aws_iam_role.task_execution_role.id
}
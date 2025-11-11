resource "aws_ecs_cluster" "application_ecs" {
  name = var.ecs_cluster

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  tags = merge(local.default_tags, {
    Name = var.ecs_cluster
  })
}

#####################################
######### task def ##################
#####################################

resource "aws_ecs_task_definition" "application_task_def" {
  family = "${var.ecs_cluster}-task-def"
  container_definitions = jsonencode([
    {
      name      = "portfolio"
      image     = var.image
      cpu       = 256
      memory    = 256
      essential = true
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
    }
  ])
  task_role_arn            = aws_iam_role.task_execution_role.arn
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  network_mode             = "awsvpc"

}

#####################################
######### service ##################
#####################################

resource "aws_ecs_service" "application_service" {
  name            = "${var.ecs_cluster}-service"
  cluster         = aws_ecs_cluster.application_ecs.id
  task_definition = aws_ecs_task_definition.application_task_def.arn
  desired_count   = 1

  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    base              = 0
    weight            = 1
  }

  network_configuration {
    subnets          = data.aws_subnets.public_subnets.ids
    security_groups  = [module.ecs_eg.security_group_id]
    assign_public_ip = true
  }
}
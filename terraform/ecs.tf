resource "aws_ecs_cluster" "application_ecs" {
  name = var.ecs_cluster

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  tags = merge(local.default_tags,{
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
      cpu       = 10
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
  task_role_arn = ""
}

#####################################
######### service ##################
#####################################

resource "aws_ecs_service" "application_service" {
  name            = "${var.ecs_cluster}-service"
  cluster         = aws_ecs_cluster.application_ecs.id
  task_definition = aws_ecs_task_definition.application_task_def.arn
  desired_count   = 1
  //iam_role        = aws_iam_role.iam.arn
  //depends_on      = [aws_iam_role_policy.]

  ordered_placement_strategy {
    type  = "binpack"
    field = "cpu"
  }

  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    base = 1
    weight = 1
  }

  network_configuration {
    subnets = []
    security_groups = []
  }
}
module "ecs_eg" {
  source       = "terraform-aws-modules/security-group/aws"
  version      = "~> 5.0"
  name         = "${var.ecs_cluster}-ecs-sg"
  description  = "ecs-sg"
  egress_rules = ["all-all"]
  ingress_with_cidr_blocks = [
    {
      from_port   = 5000
      to_port     = 5000
      protocol    = "tcp"
      description = "Allow traffic from Bastion."
      cidr_blocks = "0.0.0.0/0"
  }]
  tags = merge(local.default_tags)
}
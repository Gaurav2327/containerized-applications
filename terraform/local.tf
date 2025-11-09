locals {
  region = "us-east-1"
  default_tags = {
    resource = "ecs"
    stack    = "github-resources"
    repo_url = "containerized-applications"
  }
}
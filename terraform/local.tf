locals {
  region = "us-east-2" //region
  default_tags = {
    resource = "ecs"
    stack    = "github-resources"
    repo_url = "containerized-applications"
  }
}
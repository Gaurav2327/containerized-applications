provider "aws" {
  region = "us-east-1"
}

terraform {
  required_version = "1.12.2"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.0"
    }
  }
  # backend "s3" {
  #   key = "terraform/backend/aws-ecs.tfstate"
  #   bucket = "terraform-state-bucket-dops"
  #   encrypt = true
  #   region = "us-east-1"
  # }
}
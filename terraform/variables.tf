variable "ecs_cluster" {
  default = "application-ecs"
  type = string
  description = "ecs cluster name"
}

variable "image" {
  default = ""
  type = string
  description = "ecs image"
}


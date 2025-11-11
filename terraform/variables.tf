variable "ecs_cluster" {
  default     = "application-ecs"
  type        = string
  description = "ecs cluster name"
}

variable "image" {
  default     = "gaurav2327/myapp:559e9c857f29da5b6d72b6849d1cde2e203853b1"
  type        = string
  description = "ecs image"
}


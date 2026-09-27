variable "image_name" {
  description = "Name of the Docker image"
  type        = string
  default     = "dataops-pipeline:latest"
}

variable "container_name" {
  description = "Name of the Docker container"
  type        = string
  default     = "dataops-pipeline-container"
}
output "container_name" {
  description = "The name of the created Docker container"
  value       = docker_container.pipeline_container.name
}

output "container_id" {
  description = "The ID of the created Docker container"
  value       = docker_container.pipeline_container.id
}

output "image_name" {
  description = "The name of the Docker image used"
  value       = docker_image.pipeline_image.name
}
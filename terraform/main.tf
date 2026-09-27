resource "docker_image" "pipeline_image" {
  name = var.image_name
  build {
    context = ".."
  }
  keep_locally = true
}

resource "docker_container" "pipeline_container" {
  name     = var.container_name
  image    = docker_image.pipeline_image.image_id
  must_run = false
}
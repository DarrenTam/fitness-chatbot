variable "region" {
  description = "ap-southeast-1"
}

variable "environment" {
  description = "The Deployment environment"
}

//Networking
variable "vpc_cidr" {
  description = "The CIDR block of the vpc"
}

variable "public_subnets_cidr" {
  type        = list
  description = "The CIDR block for the public subnet"
}
variable "name" {
  description = "Name"
}

variable "container_port" {
  description = "The port of container"
}

variable "container_image" {
  description = "The name of container image"
}

variable "container_environment" {
   description = "The environment of container"
}

variable "database_table_name" {
  description = "The database table name"
}

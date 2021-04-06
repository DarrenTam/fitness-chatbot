variable "name" {
  description = "Name of the app"
}

variable "environment" {
  description = "The Deployment environment"
}

variable "vpc_id" {
  description = "The id of vpc"
}

variable "alb_arn" {
   description = "The arn of loadbalancer"
}

variable "container_port" {
 description = "The port of container"
}

variable "container_image" {
  description = "The image name of container"
}
variable "container_environment" {
   description = "The Deployment environment"
}

variable "public_subnet_all_id" {
     description = "Whole public subnet id"
}

variable "aws_alb_target_group_arn" {
    description = "Arn of alb target group"

}
variable "aws_alb_target_group" {
    description = "Alb target group"
}
locals {
  production_availability_zones = [
    "${var.region}a",
    "${var.region}b",
    "${var.region}c"]
}

module "networking" {
  source = "./modules/networking"

  region = var.region
  environment = var.environment
  vpc_cidr = var.vpc_cidr
  public_subnets_cidr = var.public_subnets_cidr
  availability_zones = local.production_availability_zones
  name = var.name
  container_port = var.container_port
}

module "database" {
  source = "./modules/database"
  name = var.name
  environment = var.environment
  database_table_name = var.database_table_name
}

module "cluster" {
  source = "./modules/cluster"
  name = var.name
  environment = var.environment
  vpc_id = module.networking.vpc_id
 alb_arn = module.networking.alb_arn
  container_port = var.container_port
  container_image = var.container_image
  container_environment = var.container_environment
  public_subnet_all_id = module.networking.public_subnet_all_id
  aws_alb_target_group_arn = module.networking.aws_alb_target_group_arn
  aws_alb_target_group = module.networking.aws_alb_target_group
}
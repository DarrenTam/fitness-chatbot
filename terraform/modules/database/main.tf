resource "aws_dynamodb_table" "user_fitness_data" {
  name = var.database_table_name
  billing_mode = "PROVISIONED"
  read_capacity = 20
  write_capacity = 20
  hash_key = "userId"

  attribute {
    name = "userId"
    type = "S"
  }

  tags = {
    Name = var.name
    Environment = var.environment
  }
}


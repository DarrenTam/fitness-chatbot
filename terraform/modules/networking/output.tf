output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "alb_arn" {
  value = aws_lb.main.arn
}

output "public_subnet_all_id" {
  value = aws_subnet.public_subnet.*.id
}

output "aws_alb_target_group_arn" {
  value = aws_alb_target_group.main.arn
}

output "aws_alb_target_group" {
  value = aws_lb.main
}
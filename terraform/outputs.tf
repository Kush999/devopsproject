output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.app.public_ip
}

output "app_url" {
  description = "URL to access the application"
  value       = "http://${aws_instance.app.public_ip}:5000"
}

output "ssh_command" {
  description = "Command to SSH into the server"
  value       = "ssh -i ~/.ssh/${var.key_name}.pem ec2-user@${aws_instance.app.public_ip}"
}
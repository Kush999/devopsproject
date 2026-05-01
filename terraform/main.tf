# =============================================
# PROVIDER - Tells Terraform we're using AWS
# =============================================
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

# =============================================
# DATA SOURCE - Get latest Amazon Linux 2 AMI
# =============================================
# Instead of hardcoding an AMI ID (which changes per region),
# we dynamically fetch the latest Amazon Linux 2 image
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# =============================================
# VPC - Your private network in AWS
# =============================================
# Think of a VPC as your own private data center
# Everything you build lives inside this network
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# =============================================
# SUBNET - A section of your VPC
# =============================================
# Public subnet = instances here CAN reach the internet
# We need this so people can access our website
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# =============================================
# INTERNET GATEWAY - Connects VPC to the internet
# =============================================
# Without this, nothing in your VPC can reach the internet
# and nobody on the internet can reach your app
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# =============================================
# ROUTE TABLE - Tells traffic where to go
# =============================================
# This says: "Any traffic going outside the VPC (0.0.0.0/0)
# should go through the Internet Gateway"
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Connect the route table to the subnet
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# =============================================
# SECURITY GROUP - Firewall rules
# =============================================
# Controls what traffic can come IN and go OUT
resource "aws_security_group" "app" {
  name        = "${var.project_name}-sg"
  description = "Allow HTTP, app port, and SSH access"
  vpc_id      = aws_vpc.main.id

  # Allow SSH (port 22) - for you to connect and debug
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTP (port 80) - standard web traffic
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow app port (5000) - where Flask runs
  ingress {
    description = "Flask App"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow ALL outbound traffic
  # The server needs to reach the internet to download
  # Docker, pull images, etc.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

# =============================================
# EC2 INSTANCE - Your actual server
# =============================================
resource "aws_instance" "app" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.app.id]
  associate_public_ip_address = true
  user_data                   = file("userdata.sh")

  tags = {
    Name = "${var.project_name}-server"
  }
}
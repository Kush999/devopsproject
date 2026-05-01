#!/bin/bash
# Update the system
yum update -y

# Install Docker
amazon-linux-extras install docker -y

# Start Docker service
systemctl start docker
systemctl enable docker

# Add ec2-user to docker group (so we don't need sudo)
usermod -aG docker ec2-user

# Pull and run the app
# For now, we'll build it directly on the server
# (Later, CI/CD will push pre-built images)

yum install -y git

# Clone your repo
git clone https://github.com/Kush999/devopsproject.git /home/ec2-user/app

# Build and run
cd /home/ec2-user/app/app
docker build -t devops-portfolio .
docker run -d -p 5000:5000 --restart=always --name portfolio devops-portfolio
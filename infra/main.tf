terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # Credentials are taken from AWS CLI config (~/.aws/credentials) on the machine
}

# ─────────────────────────────
# Security Group: proj4-ec2-sg
# ─────────────────────────────
resource "aws_security_group" "proj4_sg" {
  name        = "proj4-ec2-sg"
  description = "Allow Flask HTTP and SSH"

  ingress {
    description = "Flask HTTP"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "proj4-ec2-sg"
  }
}

# ────────────────
# proj4 EC2
# ────────────────
resource "aws_instance" "proj4_ec2" {
  ami                    = "ami-0b46816ffa1234887"  # your AMI in eu-north-1
  instance_type          = "t3.micro"
  key_name               = "proj"                  # your key pair
  vpc_security_group_ids = [aws_security_group.proj4_sg.id]

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "proj4-ec2"
  }
}

# ────────────────
# proj4 S3 Bucket
# ────────────────
resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "proj4_bucket" {
  bucket = "proj4-image-db-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_public_access_block" "proj4_bucket" {
  bucket                  = aws_s3_bucket.proj4_bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_ownership_controls" "proj4_bucket" {
  bucket = aws_s3_bucket.proj4_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "proj4_bucket" {
  bucket = aws_s3_bucket.proj4_bucket.id
  acl    = "private"

  depends_on = [
    aws_s3_bucket_public_access_block.proj4_bucket,
    aws_s3_bucket_ownership_controls.proj4_bucket
  ]
}


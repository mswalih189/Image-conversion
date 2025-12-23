provider "aws" {
  region = var.aws_region
}

resource "random_id" "suffix" {
  byte_length = 4
}

# Reference EXISTING security group (don't recreate)
data "aws_security_group" "existing_proj4_sg" {
  name = "proj4-ec2-sg"
}

resource "aws_instance" "proj4_ec2" {
  ami           = "ami-0b46816ffa1234887"
  instance_type = "t3.micro"
  key_name      = "proj"

  vpc_security_group_ids = [data.aws_security_group.existing_proj4_sg.id]

  tags = {
    Name = "proj4-ec2"
  }

  user_data = filebase64("../user_data.sh")
}

resource "aws_s3_bucket" "proj4_bucket" {
  bucket = "proj4-image-db-${random_id.suffix.hex}"
  force_destroy = true
}

resource "aws_s3_bucket_acl" "proj4_bucket" {
  bucket = aws_s3_bucket.proj4_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_ownership_controls" "proj4_bucket" {
  bucket = aws_s3_bucket.proj4_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "proj4_bucket" {
  bucket = aws_s3_bucket.proj4_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

output "ec2_public_ip" {
  value = aws_instance.proj4_ec2.public_ip
}

output "ec2_public_dns" {
  value = aws_instance.proj4_ec2.public_dns
}

output "s3_bucket_name" {
  value = aws_s3_bucket.proj4_bucket.bucket
}

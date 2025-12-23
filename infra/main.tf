provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "eu-north-1"
}

resource "random_id" "suffix" {
  byte_length = 4
}

data "aws_security_group" "existing_proj4_sg" {
  name = "proj4-ec2-sg"
}

resource "aws_instance" "proj4_ec2" {
  ami                    = "ami-0b46816ffa1234887"
  instance_type          = "t3.micro"
  key_name               = "proj"
  vpc_security_group_ids = [data.aws_security_group.existing_proj4_sg.id]

  tags = {
    Name = "proj4-ec2-${random_id.suffix.hex}"
  }

  user_data = base64encode(<<-EOF
#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
pip3 install flask boto3 pillow gunicorn

mkdir -p /opt/image_s3_app
cd /opt/image_s3_app
git clone https://github.com/mswalih189/Image-conversion.git .
pip3 install -r requirements.txt

cat > /etc/systemd/system/flask-app.service <<SERVICE
[Unit]
Description=Flask Image Conversion App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/opt/image_s3_app
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable flask-app
systemctl start flask-app
EOF
  )
}

resource "aws_s3_bucket" "proj4_bucket" {
  bucket        = "proj4-image-db-${random_id.suffix.hex}"
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
  bucket                  = aws_s3_bucket.proj4_bucket.id
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

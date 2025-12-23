output "ec2_public_ip" {
  value       = aws_instance.proj4_ec2.public_ip
  description = "Public IP for the Flask app"
}

output "ec2_public_dns" {
  value       = aws_instance.proj4_ec2.public_dns
  description = "Public DNS for the Flask app"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.proj4_bucket.bucket
  description = "S3 bucket name for images"
}



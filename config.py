import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "change-this-secret-key"
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY"
AWS_BUCKET_NAME = "YOUR_BUCKET_NAME"
AWS_REGION = "ap-south-1"

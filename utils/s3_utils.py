import boto3
import config


def upload_to_s3(file_path, filename):
    if not config.AWS_ACCESS_KEY:
        return None

    s3 = boto3.client(
        "s3",
        aws_access_key_id=config.AWS_ACCESS_KEY,
        aws_secret_access_key=config.AWS_SECRET_KEY,
        region_name=config.AWS_REGION
    )

    s3.upload_file(file_path, config.AWS_BUCKET, filename)
    return f"https://{config.AWS_BUCKET}.s3.amazonaws.com/{filename}"

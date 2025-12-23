#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
pip3 install flask boto3 pillow

# Create Flask app directory
mkdir -p /opt/image_s3_app
cd /opt/image_s3_app

# Clone your repo
git clone https://github.com/mswalih189/Image-conversion.git .
pip3 install -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/flask-app.service <<EOF
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
EOF

systemctl daemon-reload
systemctl enable flask-app
systemctl start flask-app

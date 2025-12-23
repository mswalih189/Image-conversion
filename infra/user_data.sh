#!/bin/bash
set -eux

apt-get update -y
apt-get install -y python3 python3-venv python3-pip git

APP_DIR=/opt/image_s3_app
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Clone your GitHub repo
git clone https://github.com/mswalih189/Image-conversion.git .
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Simple systemd service for Flask app
cat >/etc/systemd/system/flask-app.service <<EOF
[Unit]
Description=Flask Image App
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
Environment="FLASK_APP=app.py"
ExecStart=$APP_DIR/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable flask-app
systemctl start flask-app


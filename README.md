# Image Processing Web Application

A Flask-based web application for image editing and format conversion.

## Features
- Upload images
- Resize images
- Rotate images
- Grayscale conversion
- Compression control
- Convert image format (PNG, JPG, WEBP, BMP, TIFF)
- Ready for AWS S3 integration

## Tech Stack
- Python (Flask)
- Pillow
- SQLite (local)
- AWS S3 (optional, later)

## Run Locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

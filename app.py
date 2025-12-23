from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Convert to grayscale
            with Image.open(filepath) as img:
                gray_filename = f"gray_{filename}"
                gray_path = os.path.join(app.config['UPLOAD_FOLDER'], gray_filename)
                img.convert('L').save(gray_path)
            
            flash(f'Image converted! Download: {gray_filename}')
            return render_template('index.html', filename=gray_filename)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    """Download converted image"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        flash('File not found!')
        return redirect(url_for('index'))

@app.route('/files')
def list_files():
    """List all uploaded/converted files"""
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('files.html', files=files)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

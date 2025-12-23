from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
import os

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-2025'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('❌ Invalid credentials!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('✅ Registered! Login: admin/admin123')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('dashboard.html', files=files, username=session['username'])

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        flash('❌ No file selected!')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        flash('❌ Invalid file type!')
        return redirect(url_for('dashboard'))
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    flash(f'✅ {filename} uploaded successfully!')
    return redirect(url_for('dashboard'))

@app.route('/editor/<filename>')
def editor(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('editor.html', filename=filename)

@app.route('/process/<filename>', methods=['POST'])
def process_image(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        flash('❌ File not found!')
        return redirect(url_for('dashboard'))
    
    with Image.open(filepath) as img:
        rotate = request.form.get('rotate', '0')
        flip_h = request.form.get('flip_h')
        flip_v = request.form.get('flip_v')
        grayscale = request.form.get('grayscale')
        
        if rotate == '90':
            img = img.rotate(90, expand=True)
        elif rotate == '180':
            img = img.rotate(180, expand=True)
        elif rotate == '-90':
            img = img.rotate(-90, expand=True)
        
        if flip_h:
            img = ImageOps.mirror(img)
        if flip_v:
            img = ImageOps.flip(img)
        if grayscale:
            img = img.convert('L')
        
        new_filename = f"processed_{filename}"
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        img.save(new_path)
        flash(f'✅ Processed: {new_filename}')
    
    return redirect(url_for('dashboard'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'🗑️ {filename} deleted!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

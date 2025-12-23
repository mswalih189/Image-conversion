# utils/routes.py
import os
import uuid
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    flash,
)
from flask_login import login_required, current_user
from .image_utils import (
    load_image,
    save_temp_image,
    resize_image,
    compress_image,
    crop_image,
    enhance_image,
)

utils_bp = Blueprint(
    "utils",
    __name__,
    template_folder="../templates",
    url_prefix="/",
)


@utils_bp.route("/")
@login_required
def dashboard():
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    files = []
    for name in os.listdir(upload_folder):
        if name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            files.append(name)

    return render_template("dashboard.html", user=current_user, files=files)


@utils_bp.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("image")
    if not file or file.filename == "":
        flash("No file selected", "warning")
        return redirect(url_for("utils.dashboard"))

    # load and save as PNG locally
    img = load_image(file)
    filename = f"{uuid.uuid4().hex}.png"
    output_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    save_temp_image(img, output_path, format="PNG", quality=90)
    flash("Image uploaded!", "success")
    return redirect(url_for("utils.dashboard"))


@utils_bp.route("/edit/<filename>", methods=["GET", "POST"])
@login_required
def edit(filename):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    input_path = os.path.join(upload_folder, filename)

    if not os.path.exists(input_path):
        flash("File not found", "danger")
        return redirect(url_for("utils.dashboard"))

    # GET: show editor with live preview
    if request.method == "GET":
        return render_template("editor.html", filename=filename)

    # POST: apply edits and save a NEW file
    with open(input_path, "rb") as f:
        # wrap file to mimic FileStorage for load_image
        img = load_image(type("FS", (), {"stream": f}))

    # Resize (optional)
    width = request.form.get("width")
    height = request.form.get("height")
    if width and height:
        img = resize_image(img, width, height)

    # Crop (optional)
    left = request.form.get("left")
    top = request.form.get("top")
    right = request.form.get("right")
    bottom = request.form.get("bottom")
    if left and top and right and bottom:
        img = crop_image(img, left, top, right, bottom)

    # Tune (brightness / sharpness / contrast / blur)
    brightness_val = request.form.get("brightness") or "1.0"
    sharpness_val = request.form.get("sharpness") or "1.0"
    contrast_val = request.form.get("contrast") or "1.0"

    img = enhance_image(
        img,
        brightness=brightness_val,
        sharpness=sharpness_val,
        contrast=contrast_val,
        blur=bool(request.form.get("blur")),
    )

    # Output format + compression
    target_format = request.form.get("format", "PNG")
    quality = int(request.form.get("quality", 90))

    new_name = f"{uuid.uuid4().hex}.{target_format.lower()}"
    output_path = os.path.join(upload_folder, new_name)
    save_temp_image(img, output_path, format=target_format, quality=quality)

    flash("Image edited and saved as a new copy!", "success")
    return redirect(url_for("utils.dashboard"))

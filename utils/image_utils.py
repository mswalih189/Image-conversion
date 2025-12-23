# utils/image_utils.py
import io
import os
# [web:36][web:87][web:88]
from PIL import Image, ImageEnhance, ImageFilter, ImageStat


def load_image(file_storage):
    img = Image.open(file_storage.stream)
    return img.convert("RGBA")


def save_temp_image(img, output_path, format="PNG", quality=90):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fmt = format.upper()
    if fmt in ["JPG", "JPEG"]:
        img = img.convert("RGB")
    img.save(output_path, format=fmt, optimize=True, quality=int(quality))
    return output_path


def resize_image(img, width, height):
    width = int(width)
    height = int(height)
    return img.resize((width, height))


def compress_image(img, quality):
    bio = io.BytesIO()
    img.convert("RGB").save(bio, format="JPEG",
                            optimize=True, quality=int(quality))
    bio.seek(0)
    return bio


def crop_image(img, left, top, right, bottom):
    box = (int(left), int(top), int(right), int(bottom))
    return img.crop(box)


def enhance_image(img, brightness=1.0, sharpness=1.0, contrast=1.0, blur=False):
    # brightness
    try:
        img = ImageEnhance.Brightness(img).enhance(float(brightness))
    except Exception:
        pass

    # safe contrast (avoid ZeroDivisionError) [web:88][web:90]
    try:
        stat = ImageStat.Stat(img.convert("L"))
        if stat.count[0] > 0 and stat.mean[0] != 0:
            img = ImageEnhance.Contrast(img).enhance(float(contrast))
    except Exception:
        pass

    # sharpness
    try:
        img = ImageEnhance.Sharpness(img).enhance(float(sharpness))
    except Exception:
        pass

    if blur:
        img = img.filter(ImageFilter.GaussianBlur(radius=2))

    return img

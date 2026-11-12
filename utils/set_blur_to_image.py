from PIL import ImageFilter, ImageEnhance


def set_blur_to_image(img, bg_size=(800, 600), blur_radius=15, alpha=250):
    wh = max(bg_size)
    img = img.resize((wh, wh))
    w, h = bg_size
    max_side = max(w, h)
    left = (max_side - w) // 2
    top = (max_side - h) // 2
    img_crop = img.crop((left, top, left + w, top + h))
    img_blur = img_crop.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img_blur.putalpha(alpha)
    img = ImageEnhance.Brightness(img_blur).enhance(0.7)
    return img

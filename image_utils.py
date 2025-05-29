from PIL import Image, ImageEnhance
import numpy as np

def apply_enhancements(img, brightness, saturation, contrast):
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img_rgb = img.convert('RGB')
    img_rgb = ImageEnhance.Color(img_rgb).enhance(saturation)
    return img_rgb.convert('L')

def invert_image(img):
    arr = np.array(img)
    arr = 255 - arr
    return Image.fromarray(arr)

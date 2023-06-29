from PIL import Image
import os

def save_image(image, save_path):
    image.save(save_path)
    print(f"Image saved at {save_path}")
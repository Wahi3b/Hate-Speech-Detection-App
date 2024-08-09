from flask import current_app
import requests
import os
from PIL import Image
from io import BytesIO

def save_img(img_url, acc_handler):
    img_url = img_url.replace('_normal', '')
    response = requests.get(img_url)
    if response.status_code == 200:
        # Construct the directory path
        directory_path = os.path.join(current_app.root_path,'static', 'user_images')
        # Construct the full image path with the handler as the filename
        image_filename = f"{acc_handler}_image.jpg"
        full_image_path = os.path.join(directory_path, image_filename)

        try:
            image = Image.open(BytesIO(response.content))
            # print("Saving image to:", full_image_path)
            image.save(full_image_path)
            # print(f"Image saved at {full_image_path}")
            return full_image_path
        except IOError as e:
            print(f"An error occurred when opening or saving the image: {e}")
    else:
        # Handle cases where the image could not be fetched
        return f"Failed to fetch image: Status code {response.status_code}"

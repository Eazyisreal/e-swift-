
from PIL import Image

def resize_image(image_path, output_size=(500, 500)):
    """
    Resize the image located at image_path to the specified output_size.
    """
    img = Image.open(image_path)

    # Determine whether to crop or resize based on image dimensions
    if img.width != img.height:
        # Calculate dimensions for cropping
        if img.height > img.width:
            left = 0
            right = img.width
            top = (img.height - img.width) / 2
            bottom = (img.height + img.width) / 2
        else:
            left = (img.width - img.height) / 2
            right = (img.width + img.height) / 2
            top = 0
            bottom = img.height

        # Crop the image
        img = img.crop((left, top, right, bottom))

    # Resize the image to the specified output_size
    img.thumbnail(output_size)

    return img

def save_resized_image(image_field, output_size=(500, 500)):
    """
    Resize and save the image associated with the given image_field to the specified output_size.
    """
    img = Image.open(image_field.path)
    img = resize_image(image_field.path, output_size)
    img.save(image_field.path)

    return img

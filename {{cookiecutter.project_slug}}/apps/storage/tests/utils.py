import io

from PIL import Image


def generate_image_stub():
    file = io.BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file


def generate_file_stub():
    return generate_image_stub()

from PIL import Image
import pytesseract

class ImageReader:
    def __init__(self, path):
        self.data = pytesseract.image_to_string(Image.open(path))

    def get_data(self):
        return self.data
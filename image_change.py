#image_change.py
from PIL import Image

class ImageLoader:
    @staticmethod
    def load_image(path, max_width=None, max_height=None):
        image = Image.open(path)
        width, height = image.size
        
        if max_width or max_height:
            ratio = min(
                (max_width or width)/width,
                (max_height or height)/height
            )
            new_size = (int(width*ratio), int(height*ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            
        return image
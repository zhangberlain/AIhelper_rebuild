#image.py
from PIL import Image
import image_change
import image_in


class ImageLoadAndSend:

    
    def __init__(self,path = None):
        self.path = path

    def load(self):
        image_temp = image_change.ImageLoader()
        temp =  image_temp.load_image(self.path,1024,1024)
        temp.save(r".\image_temp\temp1001.png")#都变成png格式不就行了?
        image_return = image_in.Image_input(r".\image_temp\temp1001.png")
        imageBase64 = image_return.base64_image()
        return imageBase64
    
if __name__ == "__main__":
    x = ImageLoadAndSend(r".\photos\1012.png")
    print(x.load())

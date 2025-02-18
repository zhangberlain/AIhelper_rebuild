#image_in.py
import base64

class Image_input:

    def __init__(self,path1 = None):
        self.path = path1

    def base64_image(self):
        if  self.path == None :
            print('无图片输入')
            return None

        def encode_image(image_path):
            with open(image_path,"rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        def image_type_find(image_path):
            ends = list(image_path.split('.'))[-1]
            dic_type = {"bmp" : "bmp",
                    "dib" : "bmp",
                    "icns" : "icns",
                    "ico" : "x-icon",
                    "jfif" : "jpeg",
                    "jpe" : "jpeg",
                    "jpeg" : "jpeg",
                    "jpg" : "jpeg",
                    "j2c" : "jp2",
                    "j2k" : "jp2",
                    "jp2" : "jp2",
                    "jpc" : "jp2",
                    "jpf" : "jp2",
                    "jpx" : "jp2",
                    "apng" : "png",
                    "png" : "png",
                    "bw" : "sgi",
                    "rgb" : "sgi",
                    "rgba" : "sgi",
                    "sgi" : "sgi",
                    "tif" : "tiff",
                    "tiff" : "tiff",
                    "webp" : "webp"
                    }
            return dic_type.get(ends,None)



        base64_image = encode_image(self.path)
        image_path_end = image_type_find(self.path)

        image_url = {"url": f"data:image/{image_path_end};base64,{base64_image}"}
        return image_url

if __name__ == "__main__":
#    x = Image_input()
#    print(x.base64_image())
    pass
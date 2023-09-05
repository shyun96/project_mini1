from PIL import Image
import os

img = Image.open('./resources/humito.jpg')
img_resize = img.resize((1920,1080))

print(img_resize)

img_resize.show()










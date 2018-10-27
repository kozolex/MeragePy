import os
import random
from PIL import Image as PilImage
print(os.getcwd())

#from IPython.display import Image
#orig = Image(filename='/data/DataSet_Compare_1/3lata.1-3-split.train/blask/9Blask_21_12_2011_1.png')


#import glob, os
srcImage = PilImage.open('E:/ZIARNA/NoweStanowisko/180708/Zdrowe/00008_B.png_log2.tif')

MOD_SIZE = 200

modified = PilImage.new(srcImage.mode, (MOD_SIZE, MOD_SIZE))

angle = random.randint(-15,15) + 180 * random.randint(0, 1)

paste_x = (MOD_SIZE - srcImage.width)//2 + random.randint(-20,20)
paste_y = (MOD_SIZE - srcImage.height)//2 + random.randint(-20,20)
modified.paste(srcImage, (paste_x, paste_y))
modified = modified.rotate(angle)

print (angle)
srcImage.show()
modified.show()

#modified
#srcImage

#new_image = PilImage.new(mode, 224, 224)
#newImage.paste(srcImage, (x1,y1,x1+oldWidth,y1+oldHeight))


#print type(orig)
#print orig.mode
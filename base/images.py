import os
from PIL import Image

def compressJPG(oldPath,oldFileName,newPath,newFileName):
    im = Image.open(oldpath + '\\' + oldFileName)
    (x, y) = im.size  
    x_1 = 165
    y_1 = int(y * x_1 / x)
    out = im.resize((x_1, y_1), Image.ANTIALIAS) 
    if out.mode=='RGBA':
        out=out.convert('RGB')
    out.save('pictures_new\\{}'.format(path.split("\\")[-1]))

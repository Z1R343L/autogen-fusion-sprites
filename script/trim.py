import os
from glob import glob

from PIL import Image

trim_path = "../Battlers_trim/"
if not os.path.exists(trim_path):
    os.mkdir(trim_path)

for dir in glob("../Battlers/*"):
    for fp in glob(f"{dir}/*.png"):
        fn = fp.split("/")[-1]
        dest_path = f"{trim_path}{fn}"
        if not os.path.exists(dest_path):
            im = Image.open(fp).convert("RGBA")
            print(im.size)
            im_trim = im.crop(im.getbbox())
            im_trim.save(dest_path, "PNG")
            print(fn)
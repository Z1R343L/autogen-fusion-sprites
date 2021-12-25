import os
from glob import glob

import typer
from PIL import Image
import click_spinner
import alive_progress

src_path = '../Battlers/'
trim_path = '../Battlers_trim/'

app = typer.Typer()

def list_files() -> list:
    r = []
    for dir in glob(f"{src_path}*"):
       for fp in glob(f"{dir}/*.png"):
           r.append(fp)
    return r

@app.command()
def trim(quant: bool = False, force: bool = False) -> None:
    """trims away unused space of the sprites"""
    with click_spinner.spinner():
        pathlist = list_files()

    if not os.path.exists(trim_path):
        os.mkdir(trim_path)

    with alive_progress.alive_bar(len(pathlist)) as bar:
        for fp in pathlist:
            fn = fp.split("/")[-1]
            dest_path = f"{trim_path}{fn}"
            if not os.path.exists(dest_path) or force:
                im = Image.open(fp)
                im_trim = im.crop(im.getbbox())
                im_trim.save(dest_path, "PNG")
            bar()

if __name__ == "__main__":
    app()

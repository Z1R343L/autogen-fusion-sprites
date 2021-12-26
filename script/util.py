import os
from glob import glob

import typer
from PIL import Image
import click_spinner
from colorthief import ColorThief
import alive_progress
import srsly

src_path = '../Battlers/'
trim_path = '../Battlers_trim/'
data_path = '../Data/'

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
                if quant:
                    im_trim.convert("P", palette=Image.ADAPTIVE)
                im_trim.save(dest_path, "PNG")
            bar()

@app.command()
def index(force: bool = False) -> None:
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    pathlist = list_files()
    mons, fusions = [], []
    for fp in pathlist:
        fn = fp.split('/')[-1]
        fns = fn.split('.')
        if len(fns) == 3:
            if fns[0] == fns[1]:
                mons.append(int(fns[0]))
            else:
                fusions.append((int(fns[0]), int(fns[1])))
    srsly.write_msgpack(f"{data_path}mons.msgpack", mons)
    srsly.write_msgpack(f"{data_path}fusions.msgpack", fusions)

@app.command()
def colors(force: bool = False)-> None:
    r, pathlist = {}, glob(f"{trim_path}*.png")
    with alive_progress.alive_bar(len(pathlist)) as bar:
        for fp in pathlist:
            ct = ColorThief(fp)
            r[fp.split('/')[-1]] = ct.get_palette(color_count=2)
            bar()
    srsly.write_msgpack(f"{data_path}colors.msgpack", data=r)

if __name__ == "__main__":
    app()

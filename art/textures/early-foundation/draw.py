"""F01 / first art study. Hand-placed 32px pixel clusters; no input images.

Run from any directory: python art/textures/early-foundation/draw.py
The PNGs here are the source exports; Wiki receives identical copies.
"""
from pathlib import Path
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WIKI = ROOT / "wiki/content/assets/early-foundation"
WIKI.mkdir(parents=True, exist_ok=True)
P = {
    "ink": "#292e2e", "deep": "#414c4a", "shade": "#62716b",
    "stone": "#8b9788", "light": "#b9c2a8", "chalk": "#e1dfbd",
    "wood0": "#483b32", "wood1": "#70523a", "wood2": "#a1784b",
    "wood3": "#c69b61", "fiber0": "#786b50", "fiber1": "#b9aa78",
    "fiber2": "#e1d09a", "water0": "#344949", "water1": "#536f6b",
    "water2": "#849b88", "clay0": "#704c3c", "clay1": "#a36d4b",
    "clay2": "#cf9c6a",
}


def canvas(opaque=False):
    im = Image.new("RGBA", (32, 32), P["ink"] if opaque else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    def poly(points, c): d.polygon(points, fill=P[c])
    def rect(box, c): d.rectangle(box, fill=P[c])
    def line(points, c, width=1): d.line(points, fill=P[c], width=width)
    return im, poly, rect, line


def scrap():
    im, p, r, l = canvas()
    p([(3,17),(5,11),(10,9),(12,5),(20,4),(26,9),(28,16),(25,20),(26,23),(19,27),(10,25),(7,22),(3,22)], "ink")
    p([(5,17),(7,12),(12,11),(14,7),(20,6),(24,10),(23,16),(17,19),(10,18)], "stone")
    p([(14,7),(20,6),(23,9),(18,11),(12,12)], "light")
    p([(5,18),(10,20),(17,21),(17,25),(10,23),(8,20),(5,21)], "shade")
    p([(18,12),(24,10),(26,15),(23,19),(19,18),(18,23),(17,19)], "deep")
    p([(19,21),(23,20),(24,23),(20,25),(18,25)], "stone")
    l([(8,13),(11,14),(13,17),(16,17)], "wood2")
    l([(8,12),(11,13)], "wood3")
    l([(15,9),(15,12),(12,15)], "shade")
    l([(21,7),(24,10)], "chalk")
    r((3,26,5,27), "deep"); r((27,23,29,24), "shade")
    return im


def powder():
    im, p, r, l = canvas()
    p([(2,23),(5,20),(8,19),(10,15),(14,13),(16,9),(19,10),(21,14),(23,15),(25,19),(28,21),(30,24),(28,27),(7,28),(2,26)], "ink")
    p([(4,23),(8,21),(11,17),(15,15),(17,11),(19,12),(21,17),(24,18),(26,22),(28,23),(25,25),(9,26),(4,25)], "light")
    p([(18,13),(21,17),(24,18),(26,22),(28,23),(25,25),(14,26),(17,23),(16,21),(20,21)], "stone")
    l([(6,24),(10,23),(12,20),(15,19)], "chalk")
    l([(12,17),(15,16),(17,13)], "chalk")
    r((9,22,10,22), "stone"); r((19,24,20,24), "shade")
    r((23,21,24,21), "light"); r((13,24,14,24), "fiber1")
    r((3,17,4,18), "shade"); r((7,28,8,28), "shade")
    r((26,15,27,16), "light"); r((1,28,2,29), "stone")
    return im


def slag():
    im, p, r, l = canvas()
    p([(3,14),(6,11),(12,11),(15,9),(23,10),(27,13),(29,18),(27,24),(21,26),(11,26),(5,23),(3,20)], "ink")
    p([(5,15),(7,13),(13,13),(16,11),(23,12),(26,14),(26,19),(22,21),(11,21),(6,19)], "shade")
    p([(5,20),(11,23),(21,23),(27,20),(25,23),(20,24),(11,24),(6,22)], "deep")
    l([(6,15),(10,14),(13,15)], "stone")
    l([(17,12),(21,13),(24,13)], "stone")
    p([(9,16),(12,16),(13,18),(11,20),(8,19)], "ink")
    l([(9,19),(11,20),(13,18)], "stone")
    r((18,15,21,17), "deep"); r((18,15,20,16), "ink")
    r((15,20,17,21), "ink"); r((23,18,25,19), "ink")
    l([(5,20),(9,22),(15,22)], "wood1")
    r((25,27,27,28), "deep"); r((2,24,3,25), "shade")
    return im


def membrane():
    im, p, r, l = canvas()
    r((4,4,27,27), "ink"); r((5,5,26,26), "wood1")
    r((6,5,25,7), "wood3"); r((5,8,7,24), "wood2")
    r((8,8,23,23), "ink"); r((9,9,22,22), "fiber0")
    for x in (10,13,16,19,22): l([(x,9),(x,22)], "fiber1")
    for y in (10,13,16,19,22):
        for x in range(9,23,3): r((x,y,x+1,y), "fiber2")
    l([(8,25),(23,25)], "wood2")
    for x,y in ((6,6),(24,6),(6,24),(24,24)):
        r((x,y,x+1,y+1), "fiber1")
    r((13,2,18,3), "wood0"); r((14,2,17,2), "wood3")
    return im


def slurry():
    im, p, r, l = canvas()
    p([(4,9),(8,6),(23,6),(28,9),(29,13),(27,24),(23,28),(9,28),(5,24),(3,13)], "ink")
    p([(5,14),(9,17),(24,17),(27,14),(25,23),(22,26),(10,26),(7,23)], "clay1")
    p([(21,17),(27,14),(25,23),(22,26),(17,26),(21,22)], "clay0")
    l([(6,16),(8,22),(11,24)], "clay2")
    p([(5,10),(9,8),(23,8),(27,10),(27,13),(23,16),(9,16),(5,13)], "clay2")
    p([(7,11),(10,9),(22,9),(25,11),(24,13),(22,14),(10,14),(7,13)], "water0")
    l([(9,11),(13,10),(20,10)], "water1")
    l([(17,13),(22,13),(23,12)], "water2")
    r((11,12,13,12), "stone"); r((19,11,20,11), "shade")
    return im


def station(face):
    im, p, r, l = canvas(True)
    r((1,1,30,24), "wood1"); r((2,2,29,3), "wood3")
    r((2,5,29,23), "wood2")
    for y in (9,15,21): l([(2,y),(29,y)], "wood1")
    l([(5,6),(11,6)], "wood3"); l([(19,17),(27,17)], "wood3")
    r((1,25,30,30), "deep"); r((2,25,29,26), "stone")
    l([(2,30),(29,30)], "shade"); l([(12,27),(12,30)], "ink")
    for x in (2,27):
        r((x,3,x+2,24), "wood0"); r((x,4,x,22), "wood3")
    if face == "front":
        r((7,6,24,19), "ink"); r((8,7,23,18), "deep")
        r((9,8,22,9), "water1")
        r((9,11,14,16), "light"); r((17,11,22,16), "shade")
        r((10,11,13,12), "chalk"); r((18,13,19,14), "ink")
        l([(8,18),(23,18)], "wood3")
        r((10,21,13,22), "fiber2"); r((18,21,21,22), "stone")
        r((10,23,13,23), "wood0"); r((18,23,21,23), "wood0")
    elif face == "side":
        p([(11,8),(20,8),(24,12),(24,17),(20,21),(11,21),(7,17),(7,12)], "wood0")
        p([(12,9),(19,9),(23,13),(23,16),(19,20),(12,20),(8,16),(8,13)], "wood3")
        r((13,11,18,18), "wood1"); r((11,13,20,16), "wood1")
        r((14,13,17,16), "ink"); r((15,14,16,15), "shade")
        r((21,14,26,15), "wood0"); r((25,14,26,20), "wood0")
        r((26,16,27,19), "wood3")
    else:
        r((1,1,30,30), "wood0"); r((2,2,29,29), "wood2")
        r((3,3,28,4), "wood3"); r((3,5,4,27), "wood3")
        r((5,5,26,26), "ink"); r((6,6,25,25), "water0")
        l([(7,9),(11,8),(15,9)], "water1")
        l([(8,20),(10,21),(14,20)], "water2")
        r((17,6,24,25), "wood1"); r((18,7,23,24), "fiber0")
        for x in (19,22): l([(x,8),(x,23)], "fiber1")
        for y in (9,12,15,18,21): l([(18,y),(23,y)], "fiber2")
        r((7,12,9,14), "stone"); r((10,16,12,17), "shade")
        r((5,27,15,28), "wood3")
    return im


entries = [
    ("crude_spectrum_scrap", "粗频谱碎屑", scrap(), "item"),
    ("spectrum_powder", "石质粉料", powder(), "item"),
    ("spectrum_slag", "频谱滤渣", slag(), "item"),
    ("spectrum_membrane", "粗纤维滤框", membrane(), "item"),
    ("crude_spectrum_slurry", "泥浆批次·容器示意", slurry(), "process-icon"),
    *[(f"processing_trough_{f}", label, station(f), "block-face") for f,label in
      (("front","处理槽·收料面"),("side","处理槽·手摇侧"),("top","处理槽·投料面"))],
]
for name, _, im, _ in entries:
    assert im.size == (32, 32) and im.mode == "RGBA"
    assert all(a in (0,255) for *_,a in im.getdata()), name
    im.save(HERE / f"{name}.png")
    shutil.copyfile(HERE / f"{name}.png", WIKI / f"{name}.png")

font_path = Path("C:/Windows/Fonts/msyh.ttc")
font = ImageFont.truetype(str(font_path), 19) if font_path.exists() else ImageFont.load_default()
small = ImageFont.truetype(str(font_path), 15) if font_path.exists() else font
sheet = Image.new("RGB", (1120, 664), "#eeeade")
d = ImageDraw.Draw(sheet)
d.text((28,18), "KAMAEN / F01     第一批材料与工位 · 32 × 32 像素手绘试稿", fill="#33433e", font=font)
d.text((28,49), "从零绘制  /  大图为最近邻 4× 预览  /  右侧为原尺寸  /  游戏机制尚未接入", fill="#606958", font=small)
for i,(name,label,im,kind) in enumerate(entries):
    x = 20 + (i % 4) * 276; y = 90 + (i // 4) * 278
    d.rectangle((x,y,x+264,y+214), fill="#dfdfd2")
    for cy in range(y+12,y+156,12):
        for cx in range(x+12,x+156,12):
            c = "#d3d5c9" if ((cx-x)//12+(cy-y)//12)%2 else "#e4e4d8"
            d.rectangle((cx,cy,cx+11,cy+11), fill=c)
    sheet.paste(im.resize((128,128), Image.Resampling.NEAREST),(x+20,y+20),im.resize((128,128), Image.Resampling.NEAREST))
    sheet.paste(im,(x+197,y+27),im)
    d.rectangle((x+184,y+89,x+241,y+146),fill="#283532")
    sheet.paste(im,(x+197,y+102),im)
    d.text((x+12,y+169),label,fill="#33433e",font=font)
    d.text((x+12,y+226),kind+"  ·  草案 A",fill="#66715f",font=small)
sheet.save(HERE / "review-sheet.png")
(HERE / "manifest.json").write_text(json.dumps({
    "version":"F01-art-a", "resolution":[32,32], "status":"draft-for-review",
    "authoring":"draw.py / hand-placed pixel clusters, no input image",
    "referencePolicy":"old textures excluded", "runtimeExport":None,
    "assets":[{"id":n,"label":label,"role":role,"file":n+".png",
               "wiki":"assets/early-foundation/"+n+".png"} for n,label,_,role in entries],
},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Drew {len(entries)} fresh 32x32 textures and review-sheet.png")

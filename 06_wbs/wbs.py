from PIL import Image

tubing = Image.open('img/tubing.png').convert('RGBA')
stinger = Image.open('img/stinger.png').convert('RGBA')
packer = Image.open('img/packer.png').convert('RGBA')
port = Image.open('img/port.png').convert('RGBA')
toe = Image.open('img/toe.png').convert('RGBA')
top_cut = Image.open('img/top_cut.png').convert('RGBA')
btm_cut = Image.open('img/btm_cut.png').convert('RGBA')
perf = Image.open('img/perf.png').convert('RGBA')


def get_concat_h(im1, im2):
    dst = Image.new('RGBA', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

#get_concat_h(im1, im1).save('img/pillow_concat_h.jpg')
get_concat_v(tubing, get_concat_v(stinger, get_concat_v(packer, get_concat_v(perf, toe)))).save('img/wbs.png')
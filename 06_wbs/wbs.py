from PIL import Image
import math

tubing = Image.open('img/tubing.png').convert('RGBA')
stinger = Image.open('img/stinger.png').convert('RGBA')
packer = Image.open('img/packer.png').convert('RGBA')
port = Image.open('img/port.png').convert('RGBA')
toe = Image.open('img/toe.png').convert('RGBA')
top_cut = Image.open('img/top_cut.png').convert('RGBA')
btm_cut = Image.open('img/btm_cut.png').convert('RGBA')
perf = Image.open('img/perf.png').convert('RGBA')


def get_concat_v_multi_resize(im_list, resample=Image.Resampling.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGBA', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

wbs_length = open('wbs.csv', 'r', newline='').read().split(',').count('port')
split_max = 4
wbs_split = math.ceil(wbs_length / split_max)
start = 0
end = 0

while wbs_split > 0:
    filename = str('img/wbs' + str(wbs_split) + '.png')
    wbs_iter_list = []
    wbs_iter = open('wbs.csv', 'r', newline='').read().split(sep=',')
    for line in wbs_iter:
        if 'stinger' in line:
            wbs_iter_list.append(stinger)
        elif 'packer' in line:
            wbs_iter_list.append(packer)
        elif 'port' in line:
            wbs_iter_list.append(port)
        elif 'tubing' in line:
            wbs_iter_list.append(tubing)
        elif 'toe' in line:
            wbs_iter_list.append(toe)
        elif 'perf' in line:
            wbs_iter_list.append(perf)

    get_concat_v_multi_resize(wbs_iter_list).save(filename)
    wbs_split -= 1
#    start = end + 1
#    end = end + split_max
    print(wbs_iter_list)

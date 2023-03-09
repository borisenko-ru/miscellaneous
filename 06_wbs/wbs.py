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

split_max = 12

def get_concat_h_multi_resize(im_list, parts_num, resample=Image.Resampling.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample)
                      for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGBA', (2400 * parts_num, 1200 * (split_max + 2)))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += 2400
    return dst
def get_concat_v_multi(im_list, resample=Image.Resampling.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGBA', (2400, 1200 * (split_max + 2))) # (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += 1200
    return dst

wbs_length = open('wbs.csv', 'r', newline='').read().split(',').count('port')


wbs_iter_list = []
part_iter_list = []
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

i = 0
j = 0
while i < len(wbs_iter_list):
    if i == 0:
        elements = wbs_iter_list[i:i+split_max] + [btm_cut]
    elif i > len(wbs_iter_list) - split_max:
        elements = [top_cut] + wbs_iter_list[i:i + split_max]
    else:
        elements = [top_cut] + wbs_iter_list[i:i + split_max] + [btm_cut]
    filename = str('img/wbs' + str(j) + '.png')
    get_concat_v_multi(elements).save(filename)
    part_iter_list.append(Image.open(filename).convert('RGBA'))
    i += split_max
    j += 1
get_concat_h_multi_resize(part_iter_list, parts_num=j).save('img/wbs.png')

print(tubing.width)
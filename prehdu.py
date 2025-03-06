import json
import pandas as pd
import os

hdu_json = []

def make_name(list):
    global hdu_json
    detail = {}
    for idx in range(4, len(list)):
        if not isinstance(list[idx], str) or list[idx].find(':') == -1:
            continue
        tries = 0
        if list[idx].find('(') != -1:
            tries = int(list[idx].split('(')[1].split(')')[0]) * -1
            list[idx] = list[idx].split('(')[0]
        timelist = list[idx].split(':')
        time = int(timelist[0]) * 60 + int(timelist[1])
        detail[chr(ord('A') + idx - 4)] = {"time": time, "tries": tries}
    name, school = list[1].split(' ')
    item = {"detail": detail, "name": name, "rank": list[0], "school": school}
    hdu_json.append(item)

def transfer(filename):
    global hdu_json
    basename = os.path.basename(filename).split('.')[0]
    hdu_json = []
    pd.set_option('display.unicode.east_asian_width', True)
    hdu = pd.read_csv(filename, index_col=None, encoding='utf-8')
    hdu.apply(lambda x: make_name(x), axis=1)
    with open(f'contests/{basename}.json', 'w', encoding='utf8') as file:
        json.dump(hdu_json, file, indent=4, separators=(',', ': '), ensure_ascii=False)
    print(filename, "transfered.")

if __name__ == '__main__':
    for i in os.listdir("hdu_csv"):
        transfer("hdu_csv/" + i)

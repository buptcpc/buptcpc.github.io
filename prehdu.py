import json
import pandas as pd
import os

hdu_json = []

def make_name(list):
    global hdu_json
    detail = {}
    for idx in range(4, len(list)):
        if not isinstance(list.iloc[idx], str) or list.iloc[idx].find(':') == -1:
            continue
        tries = 0
        tmp = list.iloc[idx]
        if tmp.find('(') != -1:
            tries = int(tmp.split('(')[1].split(')')[0]) * -1
            tmp = tmp.split('(')[0]
        timelist = tmp.split(':')
        time = int(timelist[0]) * 60 + int(timelist[1])
        detail[chr(ord('A') + idx - 4)] = {"time": time, "tries": tries}
    team, name, school = list.iloc[1].split(' ')
    name = team + ' ' + name
    item = {"detail": detail, "name": name, "rank": list.iloc[0], "school": school}
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

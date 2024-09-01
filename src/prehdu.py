import json
import pandas as pd
import os

with open("config.json") as f:
    config = json.load(f)
    # hdu_contests_cids = sorted(config['hdu_contests_cids'])
    contest_dir = config['contest_dir']
    origin_dir = config['origin_dir'] + '/hdu'
    
hdu_json = []
def make_name(list):
    global hdu_json
    detail = {}
    for idx in range(4, len(list)):
        if not isinstance(list.iloc[idx], str) or list.iloc[idx].find(':') == -1:
            continue
        tries = 0
        if list.iloc[idx].find('(') != -1:
            tries = int(list.iloc[idx].split('(')[1].split(')')[0]) * -1
            list.iloc[idx] = list.iloc[idx].split('(')[0]
        timelist = list.iloc[idx].split(':')
        time = int(timelist[0]) * 60 + int(timelist[1])
        detail[chr(ord('A') + idx - 4)] = {"time": time, "tries": tries}
    # print(list.iloc[:10])
    item = {"detail": detail, "name": list['Author'].replace(' ', '   '), "rank": list['Rank']}
    hdu_json.append(item)

def transfer(filename):
    global hdu_json
    basename = os.path.basename(filename).split('.')[0]
    hdu_json = []
    pd.set_option('display.unicode.east_asian_width', True)
    hdu = pd.read_csv(filename, index_col=None, encoding='utf-8')
    hdu.apply(lambda x: make_name(x), axis=1)
    with open(f'{contest_dir}/{basename}.json', 'w', encoding='utf8') as file:
        json.dump(hdu_json, file, indent=4, separators=(',', ': '), ensure_ascii=False)
    print(filename, "transfered.")

if __name__ == '__main__':
    for file in os.listdir(origin_dir):
        transfer(f'{origin_dir}/{file}')

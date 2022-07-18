import json
import pandas as pd

hdu_json = []

def make_name(list):
    global hdu_json
    detail = {}
    for idx in range(4, len(list)):
        if not list[idx] or list[idx].find(':') == -1:
            continue
        tries = 0
        if list[idx].find('(') != -1:
            tries = int(list[idx].split('(')[1].split(')')[0]) * -1
            list[idx] = list[idx].split('(')[0]
        timelist = list[idx].split(':')
        time = int(timelist[0]) * 60 + int(timelist[1])
        detail[chr(ord('A') + idx - 4)] = {"time": time, "tries": tries}
    item = {"detail": detail, "name": list[1], "rank": list[0]}
    hdu_json.append(item)

def main():
    global hdu_json
    pd.set_option('display.unicode.east_asian_width', True)
    hdu = pd.read_csv('./hdu.csv', index_col=None, encoding='utf-8-sig')
    hdu.apply(lambda x: make_name(x), axis=1)
    with open('hd.json', 'w', encoding='utf8') as file:
        json.dump(hdu_json, file, indent=4, separators=(',', ': '), ensure_ascii=False)

if __name__ == '__main__':
    main()

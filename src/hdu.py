import requests
import json
import os
import urllib
import sys

with open("config.json") as f:
    config = json.load(f)
    hdu_contests_cids = sorted(config['hdu_contests_cids'])
    # contest_dir = config['contest_dir']
    origin_dir = config['origin_dir'] + '/hdu'

def login(cid, username, password):
    url = f"http://acm.hdu.edu.cn/contest/login?cid=" + str(cid) + "&redirect=/contest/problems%3Fcid%3D" + str(cid)
    r = requests.post(url, data = urllib.parse.urlencode({'username': username, 'password': password}),headers={
        "content-type": "application/x-www-form-urlencoded",
    }, allow_redirects=False)
    if r.status_code != 302:
        print("HDU contest " + str(cid) + " login failed.")
        return None
    return r.cookies

def export_csv(cid, filename, username, password):
    cookie = login(cid, username, password)
    if cookie is None:
        return
    url = f"http://acm.hdu.edu.cn/contest/rank?cid={cid}&export=csv"
    r = requests.get(url, cookies = cookie)
    if r.headers.get('Content-Disposition') is None or not r.headers.get('Content-Disposition').startswith("attachment"):
        print("HDU contest " + str(cid) + " is not over.")
        return

    if not os.path.isdir(origin_dir):
        os.mkdir(origin_dir)
    with open(f'{origin_dir}/{filename}.csv', "wb") as f:
        f.write(r.content)
    print("HDU contest " + str(cid) + " exported.")

def main(username, password):
    for i in range(len(hdu_contests_cids)):
        export_csv(hdu_contests_cids[i], "hd" + str(i + 1), username, password)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
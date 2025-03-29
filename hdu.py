import requests
import json
import os
import urllib
import sys
import time


def login(cid, username, password):
    url = f"http://acm.hdu.edu.cn/contest/login?cid=" + str(cid) + "&redirect=/contest/problems%3Fcid%3D" + str(cid)

    for i in range(3):
        try:
            r = requests.post(url, data = urllib.parse.urlencode({'username': username, 'password': password}),headers={
                "content-type": "application/x-www-form-urlencoded",
            }, allow_redirects=False)
            
            if r.status_code == 302:
                return r.cookies
        except:
            time.sleep(1)
    print("HDU contest " + str(cid) + " login failed.")
    return None

def export_csv(cid, filename, username, password):
    cookie = login(cid, username, password)
    if cookie is None:
        return
    time.sleep(2)
    url = f"http://acm.hdu.edu.cn/contest/rank?cid={cid}&export=csv"
    r = requests.get(url, cookies = cookie)
    if r.headers.get('Content-Disposition') is None or not r.headers.get('Content-Disposition').startswith("attachment"):
        print("HDU contest " + str(cid) + " is not over.")
        return

    if not os.path.isdir("hdu_csv"):
        os.mkdir("hdu_csv")
    with open("hdu_csv/" + filename + ".csv", "wb") as f:
        f.write(r.content)
    print("HDU contest " + str(cid) + " exported.")

def hdu_main(username, password):
    config = open("config.json", encoding='utf-8')
    hdu_contests_cids = sorted(json.load(config)['hdu_contests_cids'])
    config.close()
    
    for i in range(len(hdu_contests_cids)):
        export_csv(hdu_contests_cids[i], "hd" + str(i + 1), username, password)
        time.sleep(3)


if __name__ == "__main__":
    hdu_main(sys.argv[1], sys.argv[2])
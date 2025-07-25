import requests
import json
import os
import urllib
import sys
import time



def login(cid, username='guest', password='guest'):
    session = requests.Session()

    # 模拟浏览器的 User-Agent，防止被屏蔽
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"http://acm.hdu.edu.cn/contest/login?cid={cid}"
    }

    url = f"http://acm.hdu.edu.cn/contest/login?cid={cid}&redirect=/contest/problems%3Fcid%3D{cid}"
    payload = {
        'username': username,
        'password': password
    }

    for _ in range(3):
        try:
            r = session.post(url, data=urllib.parse.urlencode(payload), headers=headers, allow_redirects=False)
            if r.status_code == 302:  # 登录成功，会重定向
                return session.cookies
            else:
                print(f"Try failed: Status {r.status_code}")
        except Exception as e:
            print(f"Exception during login: {e}")
            time.sleep(1)

    print(f"HDU contest {cid} login failed.")
    return None

def export_csv(cid, filename, username, password):
    cookie = login(cid)
    if cookie is None:
        return
    time.sleep(2)
    url = f"http://acm.hdu.edu.cn/contest/rank?cid={cid}&export=csv"


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"http://acm.hdu.edu.cn/contest/login?cid={cid}"
    }

    r = requests.get(url, cookies = cookie, headers=headers)
    print(r)
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
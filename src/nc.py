import requests
import json
import re
import os

ALL = 32
with open("config.json") as f:
    config = json.load(f)
    contest_dir = config['contest_dir']

def work(cid, index):
    ranks = {}
    for i in range(ALL):
        url = f'https://ac.nowcoder.com/acm-heavy/acm/contest/real-time-rank-data?token=&id={cid}&page={i + 1}&limit=0&_=1626692170101'
        res = requests.get(url)
        data = res.json().get('data', {})
        rank_data = data.get('rankData', [])
        problem_data = data.get('problemData', [])
        contest_begin_time = data.get('basicInfo', {}).get('contestBeginTime', 0)

        for o in rank_data:
            d = {}
            for j, problem in enumerate(problem_data):
                accepted_time = o['scoreList'][j]['acceptedTime']
                d[problem['name']] = {
                    'time': accepted_time if accepted_time == -1 else (accepted_time - contest_begin_time) // 1000 // 60,
                    'tries': o['scoreList'][j]['failedCount']
                }
            # print(o)
            ranks[o['ranking']] = {
                'detail': d,
                'name': o['userName'],
                'school': o.get('school', ''),
                'rank': o['ranking']
            }

    arr = [ranks[key] for key in ranks]
    if len(arr) == 0:
        print(f'nowcoder contest {cid} is not over.')
        return

    with open(f'{contest_dir}/nc{index + 1}.json', 'w', encoding='utf-8') as f:
        json.dump(arr, f, ensure_ascii=False)
    print(f'nowcoder contest {cid} exported.')

def search_contests(keyword):
    url = f'https://ac.nowcoder.com/acm-heavy/acm/contest/search-detail?searchName={requests.utils.quote(keyword)}&topCategoryFilter=13'
    res = requests.get(url)
    regexp = r'<a href="/acm/contest/(\d+?)" target="_blank">(\d+?)</a>'
    matches = re.findall(regexp, res.text)
    cids = sorted([match[0] for match in matches], key=lambda x: int(x))
    
    for index, cid in enumerate(cids):
        work(cid, index)

# work(cid)

search_contests("2024牛客暑期多校训练营")

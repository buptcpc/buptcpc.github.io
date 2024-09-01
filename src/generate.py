import os
import json

# 读取 contests 目录下的所有文件

spring_contests = ['vj6', 'vj8', 'vj9', 'vj10', 'vj11', 'vj12']
summer_contests = ['hd2', 'hd3', 'hd4', 'hd5', 'hd6', 'hd7', 'hd8', 'hd9', 'hd10', 'nc3', 'nc4', 'nc5', 'nc6', 'nc7', 'nc8', 'nc9', 'nc10']

with open("config.json", encoding='utf-8') as f:
    config = json.load(f)
    # hdu_contests_cids = sorted(config['hdu_contests_cids'])
    contest_dir = config['contest_dir']
    # origin_dir = config['origin_dir'] + '/hdu'

arr = os.listdir(contest_dir)

def load_contests(contests, belong_name):
    teams = set()
    conts = []
    table_data = []
    scores = {}
    team_stats = {}

    def load(contest):
        team_stats[contest] = {}
        conts.append(contest)
        with open(f'{contest_dir}/{contest}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        prob_count = 0
        acc = {}
        max_solved = 0
        teams_count = 0

        while chr(prob_count + ord('A')) in data[0]['detail']:
            acc[chr(prob_count + ord('A'))] = 0
            prob_count += 1

        for item in data:
            solved = 0
            for prob, detail in item['detail'].items():
                if detail['time'] != -1:
                    acc[prob] = acc.get(prob, 0) + 1
                solved += 1
            max_solved = max(max_solved, solved)
            if solved > 0:
                teams_count += 1

        teams_number = {
            "vj6": 82,
            "vj8": 42,
            "vj9": 244,
            "vj10": 252,
            "vj11": 184,
            "vj12": 198,
        }

        if "vj" in contest:
            teams_count = teams_number.get(contest, teams_count)

        print(contest, max_solved, teams_count)

        bupt_hdu = {
            "team304": "摩可彭塔斯（区庆亮，鲍睿钊，谭怡萱）",
            "team303": "网瘾犯了求求你把牌子给我（刘益铭，陈杰祥，谢志宏）",
            "team302": "彰显王威吧，踏遍世间的十二辉剑！（张颢龄，谢牧航，王若竹）",
            "team310": "遥遥领先于友队（王昰妍，梁浩然，李鹏烁）",
            "team307": "好好想想（司睿洋，尹昱钦，张泽文）",
            "team313": "堂吉诃德（卢安来，王冀恒，管庆涵）",
            "team309": "帮帮我，评测机老爷爷！（田苗，曾巍，蔡禹煊）",
            "team306": "[AI]GPT4o（袁桦斌，杨毅霖，马骐荣）",
            "team312": "如果爆零能报销回家车费吗（赵佳一，陈育堃，李天阳）",
            "team305": "试者如斯夫，不舍昼夜（安澍，秦维斌，李泽林）",
            "team308": "世界其实是一个巨大的华为手机（赵瑞霖，李乐扬，张智成）",
            "team301": "嘉然今天吃汉堡（王智炜，胡诚成，李博识）",
            "team413": "我宣布以上成绩无效（田艺彬，王华德，李子俊）",
            "team314": "歪日，这么虾头？（安奕轩，谢楠，林米乐）",
            "team319": "金牌厨师（乔函祺，李思远，马铂凯）",
            "team315": "DP_PTSD（王垚烨，蒙忠格，黄志阳）",
            "team316": "吃堡没吃饱（吴优，单一凡，金旭一）",
            "team318": "我太想AC了（马云霄，侯尔为，刘奕安）",
            "team317": "4000g_Pt（冯国晟，于洋，马廷良）",
            "team311": "对了没？如队（曾行周，钱文韬，徐衍巅）",
        }
        bupt_nc = {
            "team304": "Mocopentas",
            "team303": "网瘾犯了求求你把牌子给我",
            "team302": "彰显王威吧，踏遍世间的十二辉剑",
            "team310": "遥遥领先于友队",
            "team307": "好好想想_",
            "team313": "Don_Quixote",
            "team309": "帮帮我，测评机老爷爷！",
            "team306": "[AI]GPT4o",
            "team312": "如果爆零能报销回家车费吗",
            "team305": "逝者如斯夫不舍昼夜",
            "team308": "世界其实是一个巨大的华为手机",
            "team301": "嘉然今天吃汉堡",
            "team413": "我宣布以上成绩无效",
            "team314": "歪日，这么虾头？",
            "team319": "金牌厨师",
            "team315": "DP_PTSD",
            "team316": "Humgry",
            "team318": "我太想AC了",
            "team317": "4000g_PT",
            "team311": "对了没？如队",
        }
        bupt_vj = {
            "team304": "mocopentas",
            "team303": "pair_Ac_Ac",
            "team302": "Joyeuse_Ordre",
            "team310": "Liangsheng298",
            "team307": "_nepenthe_",
            "team313": "Don_Quixote",
            "team309": "zengwei1",
            "team306": "three_newbie",
            "team312": "yidau",
            "team305": "neetman",
            "team308": "nzot",
            "team301": "UltraCat",
            "team413": "err_Grade",
            "team314": "Bush_Gamma",
            "team319": "O_start",
            "team315": "DP_PTSD",
            "team316": "Humgry",
            "team318": "WeMissAcSoMuch",
            "team317": "4000g_Pt",
            "team311": "void_WarmUp",
        }
        
        high = -1
        for item in data:
            rank = int(item['rank'])
            cnt = sum(1 for prob, detail in item['detail'].items() if detail['time'] != -1)
            score = max(0, cnt * (500 - rank))
            if high == -1:
                high = score
            score = score / high * 100

            if "vj" in contest:
                score = max(0, 100 * cnt / max_solved * ((teams_count - rank + 1) / teams_count))  # 2024 春季训练计分方式

            if "hd" in contest:
                item['name'], item['school'] = tuple(item['name'].split('   '))
                if item['name'] in bupt_hdu:
                    item['name'] = bupt_hdu[item['name']]
            
            if 'vj' in contest:
                item['school'] = "北京邮电大学";
                item['name'] = item['name'].split('(')[0]

            hdu_name = ""
            if item.get('school', '') == "北京邮电大学": 
                if item['name'] in bupt_hdu.values():
                    hdu_name = item['name']
                elif item['name'] in bupt_nc.values():
                    for key, value in bupt_nc.items():
                        if value == item['name']:
                            hdu_name = bupt_hdu[key]
                elif item['name'] in bupt_vj.values():
                    item['school'] = "北京邮电大学"
                    for key, value in bupt_vj.items():
                        if value == item['name']:
                            hdu_name = bupt_hdu[key]

            if not hdu_name:
                continue

            teams.add(hdu_name)
            team_stats[contest][hdu_name] = f"{item['rank']}/{cnt}/{score:.2f}"
            found = False
            for t in table_data:
                if t['name'] == hdu_name:
                    found = True
                    scores[hdu_name].append(float(f"{score:.2f}"))
            if not found:
                scores[hdu_name] = [0] * (len(conts) - 1)
                scores[hdu_name].append(float(f"{score:.2f}"))
                table_data.append({"name": hdu_name, "type": "line", "data": scores[hdu_name], "markLine": {"data": [{"type": "average", "name": "平均值"}]}})

        for t in table_data:
            if len(t['data']) != len(conts):
                t['data'].append(0)

    for i in arr:
        contest_name = i.split('.')[0]
        if contest_name in contests:
            load(contest_name)
            print(f"{belong_name} contest {contest_name} generated.")

    with open(f'data/{belong_name}_stat.json', 'w', encoding='utf-8') as f:
        json.dump({
            "teams": list(teams),
            "conts": conts,
            "data": table_data,
            "scores": scores,
            "teamStats": team_stats
        }, f, ensure_ascii=False)

load_contests(spring_contests, 'spring')
load_contests(summer_contests, 'summer')

import os
import json
import math
from pathlib import Path

def load_contest(contest_path, config_teams, school_name, need_all_team):
    with open(contest_path, 'r', encoding='utf-8') as f:
        contest_data = json.load(f)
    
    processed_teams = []
    for team in contest_data:
        solved = 0
        penalty = 0
        for problem in team['detail'].values():
            if problem['time'] >= 0:
                solved += 1
                penalty += problem['tries'] * 20 + problem['time']
        if solved == 0:
            continue
        processed_teams.append({
            'name': team['name'],
            'solved': solved,
            'penalty': penalty,
            'school': team.get('school', '')
        })
    
    substrings = set()
    for t in config_teams:
        substrings.add(t['name'])
        for alias in t.get('alias', []):
            substrings.add(alias)
    
    filtered_teams = []
    if need_all_team == True:
        filtered_teams = processed_teams
    else:
        filtered_teams = []
        for pt in processed_teams:
            for substr in substrings:
                if substr in pt['name']:
                    if need_all_team == False and (pt['school'] == '' or pt['school'] == school_name):
                        filtered_teams.append(pt)
                        break
    
    if not filtered_teams:
        return {}, 0, 0
    
    sorted_teams = sorted(filtered_teams, key=lambda x: (-x['solved'], x['penalty']))
    
    max_problem_solved = 0
    if need_all_team == True:
        max_problem_solved = sorted_teams[0]['solved']

    if sorted_teams:
        sorted_teams[0]['rank'] = 1
        prev_solved = sorted_teams[0]['solved']
        prev_penalty = sorted_teams[0]['penalty']
        current_rank = 1
        
        for i in range(1, len(sorted_teams)):
            team = sorted_teams[i]
            if team['solved'] == prev_solved and team['penalty'] == prev_penalty:
                team['rank'] = current_rank
            else:
                current_rank = i + 1
                team['rank'] = current_rank
                prev_solved = team['solved']
                prev_penalty = team['penalty']
    
    
    result_map = {}
    for ct in config_teams:
        team_substrings = [ct['name']]
        for alias in ct.get('alias', []):
            team_substrings.append(alias)
        matched = []
        for st in sorted_teams:
            for substr in team_substrings: 
                if substr in st['name'] and (st['school'] == '' or st['school'] == school_name):
                    matched.append(st)
                    break
        
        if not matched:
            continue
        
        best_team = sorted(matched, key=lambda x: (-x['solved'], x['penalty']))[0]
        result_map[ct['name']] = [best_team['solved'], best_team['rank']]
        if need_all_team == False:
            max_problem_solved = max(max_problem_solved, best_team['solved'])
    
    print(len(filtered_teams), 'teams from', contest_path.stem)
    print('Max problem solved:', max_problem_solved)
    return result_map, max_problem_solved, len(filtered_teams)

def get_contests_info():
    contests_dir = Path('contests')
    config_path = Path('.') / 'config.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    config_teams = config['teams']
    school_name = config['school']
    need_all_team = config.get('need_all_team', True)
    maximum_rank = config.get('maximum_rank', -1)
    
    contest_files, contest_names = [], []
    for f in contests_dir.glob('*.json'):
        contest_files.append(f)
        contest_names.append(f.stem)
    
    result = {}
    for cf in contest_files:
        contest_name = cf.stem
        result[contest_name] = load_contest(cf, config_teams, school_name, need_all_team)

    # contest_names，以前缀英文为第一关键字、后缀数字为第二关键字排序，如['hd1', 'vj10', 'nc999']
    contest_names.sort(key = lambda x:
        (x[:-2], int(x[-2:])) if x[-2:].isdigit() else (x[:-1], int(x[-1:]))
    )
    return config_teams, contest_names, result, maximum_rank

def generate_stat_json(teams_dict, contests_names, data, maximum_rank):
    teams = []
    for team in teams_dict:
        teams.append(team['name'])
    # 处理每个比赛，获取对应的分数字典
    contest_scores_map = {}
    for contest_name in contests_names:
        contest_data, max_problem_solved, total_teams = data.get(contest_name, [{}, 0, 0])
        if maximum_rank != -1:
            total_teams = min(total_teams, maximum_rank)
        contest_scores_map[contest_name] = get_contest_score(contest_name, contest_data, max_problem_solved, total_teams)

    # 生成每个队伍的分数列表
    scores_dict = {}
    for team in teams:
        team_scores = []
        for contest_name in contests_names:
            # 从对应比赛的分数字典中获取分数，不存在则为0.0
            score = contest_scores_map[contest_name].get(team, 0.0)
            team_scores.append(score)
        scores_dict[team] = team_scores

    # 构建图表数据部分
    data_list = []
    for team in teams:
        entry = {
            "name": team,
            "type": "line",
            "data": scores_dict[team],
            "markLine": {
                "data": [{"type": "average", "name": "平均值"}]
            }
        }
        data_list.append(entry)

    # 生成队伍统计信息 teamStats
    team_stats = {}
    for contest_name in contests_names:
        contest_data, max_solved, teams_num = data.get(contest_name, {})
        print(contest_data)
        contest_scores = contest_scores_map[contest_name]
        contest_entry = {}
        for team in teams:
            if team in contest_data:
                solved = contest_data[team][0]
                rank = contest_data[team][1]
                score = contest_scores.get(team, 0.0)
                contest_entry[team] = f"{rank}/{solved}/{score}"
            else:
                contest_entry[team] = "?/?/?"
        team_stats[contest_name] = contest_entry

    # 计算每个队伍的总分
    total_score_dict = {}
    for team in teams:
        total_score = get_total_score(contests_names, scores_dict[team])
        total_score_dict[team] = total_score

    # 构建最终的JSON结构
    result = {
        "teams": teams,
        "conts": contests_names,
        "data": data_list,
        "scores": scores_dict,
        "teamStats": team_stats,
        "total_score": total_score_dict
    }

    return result

def get_contest_score(contest_name, contest_data, max_problem_solved, total_teams):
    # score = problem_solved / max_problem_solved * max(0, atleast_one_solved_count - rank + 1) / atleast_one_solved_count (if atleast_one_solved_count = 0 then 0)
    score = {}
    if not contest_data:
        return score
    for team, v in contest_data.items():
        if total_teams == 0:
            score[team] = 0
        else:
            # print(v[1], total_teams, team)
            tmp = v[0] / max_problem_solved * max(0, total_teams - v[1] + 1) / max(1, total_teams) * 100
            # 2位小数
            score[team] = round(tmp, 2)
    return score

def get_total_score(contest_name, scores):
    # 取前4/5个比赛的分数的平均值
    if not scores or not contest_name:
        return 0.0
    contests_num = len(contest_name)
    need_contests_num = max(int(math.ceil(contests_num * 4 / 5)), 1)
    sorted_scores = sorted(scores, reverse=True)
    return round(sum(sorted_scores[:need_contests_num]) / need_contests_num, 2)

def main():
    teams, contest_names, data, maximum_rank = get_contests_info()
    result = generate_stat_json(teams, contest_names, data, maximum_rank)
    
    # 写入JSON文件
    with open('stat.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
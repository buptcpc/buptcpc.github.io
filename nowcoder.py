import requests
import json
import os
import re
from urllib.parse import quote

ALL = 32  # 总页数配置

def process_contest_data(cid, index):
    """处理单个比赛数据"""
    session = requests.Session()
    ranks = {}
    
    try:
        # 分页获取所有数据
        for page in range(1, ALL+1):
            url = f"https://ac.nowcoder.com/acm-heavy/acm/contest/real-time-rank-data?token=&id={cid}&page={page}&limit=0"
            response = session.get(url, timeout=10)
            response.raise_for_status()  # 检查HTTP错误
            
            data = response.json().get('data', {})
            problem_data = data.get('problemData', [])
            basic_info = data.get('basicInfo', {})
            
            for record in data.get('rankData', []):
                detail = {}
                for idx, problem in enumerate(problem_data):
                    score = record['scoreList'][idx]
                    accepted_time = score.get('acceptedTime', -1)
                    
                    # 计算解题时间（分钟）
                    time = -1
                    if accepted_time != -1:
                        start_time = basic_info.get('contestBeginTime', 0)
                        time = (accepted_time - start_time) // 60000  # 毫秒转分钟
                        
                    detail[problem['name']] = {
                        'time': time,
                        'tries': score.get('failedCount', 0)
                    }
                
                ranks[record['ranking']] = {
                    'detail': detail,
                    'name': record['userName'],
                    'school': record.get('school', ''),
                    'rank': record['ranking']
                }
        
        # 转换并保存数据
        if not ranks:
            print(f"比赛 {cid} 无有效数据")
            return

        output = list(ranks.values())
        os.makedirs('contests', exist_ok=True)
        filename = os.path.join('contests', f'nc{index+1}.json')
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        print(f"比赛 {cid} 数据已保存至 {filename}")

    except Exception as e:
        print(f"处理比赛 {cid} 时出错: {str(e)}")

def fetch_contests(keyword):
    """获取匹配的比赛列表"""
    try:
        url = f"https://ac.nowcoder.com/acm-heavy/acm/contest/search-detail?searchName={quote(keyword)}&topCategoryFilter=13"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 使用正则提取比赛ID
        pattern = re.compile(r'/acm/contest/(\d+)"')
        cids = list(set(pattern.findall(response.text)))
        return sorted(cids, key=int)  # 按数字排序
        
    except Exception as e:
        print(f"获取比赛列表失败: {str(e)}")
        return []

def load_config():
    """读取配置文件"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            keyword = config.get('nowcoder_contests', '')
            
            if not isinstance(keyword, str):
                raise ValueError("配置格式错误: nowcoder_contests 应为字符串")
                
            return keyword
    except Exception as e:
        print(f"读取配置文件失败: {str(e)}")
        raise

def main():
    """主执行函数"""
    try:
        keyword = load_config()
        print(f"当前配置关键字: {keyword}")
        
        cids = fetch_contests(keyword)
        if not cids:
            print("未找到匹配的比赛")
            return
            
        print(f"找到 {len(cids)} 个比赛: {', '.join(cids)}")
        
        # 依次处理每个比赛
        for idx, cid in enumerate(cids):
            print(f"正在处理比赛 {cid} ({idx+1}/{len(cids)})...")
            process_contest_data(cid, idx)
            
    except Exception as e:
        print(f"程序执行失败: {str(e)}")

if __name__ == '__main__':
    main()
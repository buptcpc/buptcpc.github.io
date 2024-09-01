import requests
import json
import os
import urllib
import sys
from functools import cmp_to_key
import pandas as pd

with open("config.json") as f:
    config = json.load(f)
    # hdu_contests_cids = sorted(config['hdu_contests_cids'])
    contest_dir = config['contest_dir']
    origin_dir = config['origin_dir'] + '/vj'
    
question_cols = []

def time2num(time):
    # print(time.__repr__())
    hour, minute, second = tuple(map(int, time.split(':')))
    return hour * 60 + minute + second / 60

def row2object(row):
    def process(val):
        val2 = val.strip().removesuffix(')').split('(-')
        if val2[0] == '':
            return None

        match len(val2):
            case 1:
                return {
                    'tries': 0,
                    'time': time2num(val2[0])
                }
            case 2:
                return {
                    'tries': int(val2[1]),
                    'time': time2num(val2[0])
                }
            case _:
                raise ValueError('Find a group with Error question value ' + val)
    
    return {
        'rank': row['Rank'] + 1,
        'name': row['Team'],
        'detail': { question: process(row[question]) for question in question_cols if process(row[question])}
    }
    
def transfer(contest, supplement, result_json):
    origin_df = pd.read_excel(contest, header = [0, 1], index_col = 0)
    origin_df.columns = map(lambda x: x[0], origin_df.columns)
    if os.path.exists(supplement):
        supplement_df = pd.read_excel(supplement, header = [0, 1], index_col = 0)
        supplement_df.columns = map(lambda x: x[0], supplement_df.columns)
        # print(origin_df.loc[:10])
        
        assert (origin_df.columns == supplement_df.columns).all(), 'Two sheet need to have same header'
        
        merged = pd.concat([origin_df, supplement_df]).fillna(value = '').map(str)
        # print(merged.loc[:10])
        
        sort = merged.sort_values(by = ['Score', 'Penalty'], ascending=[False, True])
        # print(sort.iloc[:10])
    else:
        sort = origin_df

    indexed = sort.reset_index(drop = True).reset_index(names = 'Rank')
    # print(indexed.loc[:10])

    global question_cols
    question_cols = indexed.columns[4:].to_list()
    # print(question_cols)
    result = indexed.apply(row2object, axis = 1).to_list()

    with open(result_json, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
        
    print(f'{contest} with {supplement} to {result_json} transfer complete.')

if __name__ == "__main__":
    for file in os.listdir(origin_dir):
        if not file.startswith('supplement_'):
            file = file.removesuffix(".xlsx")
            transfer(
                f'{origin_dir}/{file}.xlsx', 
                f'{origin_dir}/supplement_{file}.xlsx',
                f'{contest_dir}/{file}.json'
            )
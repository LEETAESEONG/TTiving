import pandas as pd

file1  = 'KC_502_LLR_MOVIE_DRMA_PLCE_2022.csv'

df = pd.read_csv(file1)
# id, POI명, 시도명, 시군구명, 법정동명, 리명, 번지번호, 위치경도, 위치위도
new_df = df[['ID','POI_NM','CTPRVN_NM','SIGNGU_NM','LEGALDONG_NM','LI_NM','LNBR_NO','LC_LO','LC_LA']]
# print(new_df.columns)

with open('tmp.json', 'w', encoding='utf-8') as f:
    new_df.to_json(f, force_ascii=False, orient='records')

import json

file_path = 'tmp.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    # print(type(data))
    # print(data)

result = []

for i in range(len(data)):
    # print(d)
    result.append({"model":"movies.MovieLocation", "pk":i+1, "fields":data[i]})

with open('./filming_location.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
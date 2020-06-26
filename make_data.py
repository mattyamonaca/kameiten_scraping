import os
import pandas as pd
import yaml

file_list = os.listdir(path = "./tmp/")
with open("./conf.yaml") as f:
    conf = yaml.safe_load(f)

df_list = []
for name in file_list:
    df = pd.read_csv("./tmp/" + name,encoding="cp932")
    df_list.append(df)

result = pd.concat(df_list)

dup = len(result[result["id"].duplicated()])
length = len(result)

print("--- 重複削除前 ---")
print("データ総数 : {}".format(length))
print("重複件数 : {}".format(dup))


result = result[~result.duplicated(subset="id")]

dup = len(result[result["id"].duplicated()])
length = len(result)

print("--- 重複削除後 ---")
print("データ総数 : {}".format(length))
print("重複件数 : {}".format(dup))

with open("output/output_{}.csv".format(conf["prefecture"]),mode="w",encoding="cp932",errors="ignore") as f:                                                                                                           
        result.to_csv(f,index=None) 


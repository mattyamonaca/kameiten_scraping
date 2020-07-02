import os
import pandas as pd
import yaml

#file_list = os.listdir(path = "./tmp/")
with open("./conf.yaml") as f:
    conf = yaml.safe_load(f)


def remove_duplicate(cd):
    file_list = os.listdir(path = "./tmp/code_{}".format(cd))
    df_list = []
    for name in file_list:
        df = pd.read_csv("./tmp/code_{}/".format(cd) + name,encoding="cp932")
        df_list.append(df)

    result = pd.concat(df_list)

    dup = len(result[result.duplicated()])
    length = len(result)

    print("--- 重複削除前 ---")
    print("データ総数 : {}".format(length))
    print("重複件数 : {}".format(dup))


    result.drop_duplicates(inplace=True)

    dup = len(result[result.duplicated()])
    length = len(result)

    print("--- 重複削除後 ---")
    print("データ総数 : {}".format(length))
    print("重複件数 : {}".format(dup))

    return result


if conf["prefecture"] == "all":
    prefecture_df = pd.read_csv("./prefecture_list.csv")
    prefecture_list = prefecture_df["Code"]
    for cd in prefecture_list:
        result = remove_duplicate(cd)
        with open("output/output_{}.csv".format(cd),mode="w",encoding="cp932",errors="ignore") as f:                                   
            result.to_csv(f,index=None)
else:
    result = remove_duplicate(conf["prefecture"])
    with open("output/output_{}.csv".format(conf["prefecture"]),mode="w",encoding="cp932",errors="ignore") as f:                                   
        result.to_csv(f,index=None)



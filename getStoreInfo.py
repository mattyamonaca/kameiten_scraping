import requests
import json
from urllib import parse
import pandas as pd
import codecs
import time
import yaml
import os

from tqdm import tqdm
#appid = "dj00aiZpPU9lblRWbnBmYU9SOSZzPWNvbnN1bWVyc2VjcmV0Jng9ZTI-"


def checkKey(obj,key):
    if key in obj:
        return obj[key]
    else:
        return None
    


def getStoreInfos(gc,ac,start):
    payload = {
        "callback" : "jquery1592447040102",
        "output" : "jsonp",
        "appid" : "mYtGHwmxg6412C5A6JqgvhnCBS4705tleP6LsC6ZSsKh.yfvcXI.nIYjYibv8A--",
        "detail" : "full",
        "sort" : "hybrid",
        "distinct" : "shortcut",
        "group" : "gid",
        "results" : "100",
        "exclude_seireishi" : "false",
        "start" : start,
        "sc" : "",
        "gc" : gc,
        "bid" : "",
        "cid" : "",
        "ac" : ac,
        "dist" : "",
        "lat" : "",
        "lon" : "",
        "exact_text2" : "",
        "query" : "",
        "bbox" : "",
        "page" : "",
        "uid" : "",
        "coupon" : "",
        "parking" : "",
        "creditcard" : "",
        "open" : "",
        "minprice" : "",
        "maxprice" : "",
        "id" : "",
        "overflow" : "",
        "floor" : "",
        "aml" : "",
        "recursive" : ""
        }
   
#gid = "rwngV12Va6Q&_i=1&_=1592447040100"
    gid = ""
   
   
    url = "https://map.yahoo.co.jp/api/localsearch?" + parse.urlencode(payload) + "&gid={}".format(gid)

    #print(url)

    response = requests.get(url)
    #shop_num = response.count('id')
    suffix = response.text.split("(")[0] + "("
    json_f = response.text.replace(suffix,"").rstrip(")")
   
    elements = json.loads(json_f)

    
#print(elements)
    if "Feature" not in elements.keys():
        return None

    key_list = elements["Feature"][0].keys()

    header_list = [
        "id",
        "gid",
        "name",
        "latitude",
        "longitude",
        "address",
        "paypay_flg",
        ]
   
    id_list = []
    gid_list = []
    name_list = []
    latitude_list = []
    longitude_list = []
    address_list = []
   
    station_id_list = []
    station_name_list = []
    station_distance_list = []
    station_time_list = []
   
    genre_code_list = []
    genre_name_list = []
   

    review_count_list = []
    access_list = []
   
    paypay_flg_list = []
   

   
   

    for element in elements["Feature"]:
        id_list.append(element["Id"])
        gid_list.append(element["Gid"])
        name_list.append(element["Name"])
        coordinates = element["Geometry"]["Coordinates"].split(",")
        longitude_list.append(coordinates[0])
        latitude_list.append(coordinates[1])
        property = element["Property"]

       
        if "Address" in property.keys():
            address_list.append(property["Address"])
        else:
            address_list.append(None)

        if "Station" in property.keys() and len(element["Property"]["Station"]) > 0:
            station = element["Property"]["Station"][0]
            station_id_list.append(checkKey(station,"Id"))
            station_name_list.append(checkKey(station,"Name"))
            station_distance_list.append(checkKey(station,"Distance"))
            station_time_list.append(checkKey(station,"Time"))
        else:
            station_id_list.append(None)
            station_name_list.append(None)
            station_distance_list.append(None)
            station_time_list.append(None)

        if "Genre" in property.keys():
            genre = element["Property"]["Genre"][0]
            genre_code_list.append(checkKey(genre,"Code"))
            genre_name_list.append(checkKey(genre,"Name"))
        else:
            genre_code_list.append(None)
            genre_name_list.append(None)

        if "LocoReviewCount" in property.keys():
            rc = property["LocoReviewCount"]
            review_count_list.append(rc)
        else:
            review_count_list.append(None)
       
        if "Access1" in property.keys():
            access_list.append(property["Access1"])
        else:
            access_list.append(None)
           
        if "PayPayFlag" in property["Detail"].keys():
            if property["Detail"]["PayPayFlag"] == "true":
                paypay_flg_list.append(True)
            else:
                paypay_flg_list.append(False)
        else:
            paypay_flg_list.append(False)
           
    store_info_dict = {
        "id":id_list,
        "gid":gid_list,
        "name":name_list,
        "latitude":latitude_list,
        "longitude":longitude_list,
        "address":address_list,
        "satation_id":station_id_list,
        "station_name":station_name_list,
        "station_distance":station_distance_list,
        "station_time":station_time_list,
        "genre_code" : genre_code_list,
        "genre_name" : genre_name_list,
        "review_count" : review_count_list,
        "access" : access_list,
        "paypay_flg":paypay_flg_list,
        }

    df = pd.DataFrame(store_info_dict)
   
       
    return df


#if __name__ == "__main__":

def run(conf,prefecture):
    #with open("./conf.yaml") as f:
    #    conf = yaml.safe_load(f)
    #print(conf)

    genre_cd = pd.read_csv("./genre.csv")

    #gc取得
#    gc_list = ["01", "02", "03", "04"]
    gc_list = genre_cd["業種コード2"].unique().tolist()
    print(gc_list)
    print("gc総数 {}".format(len(gc_list)))
    
    
    #ac取得
    path = "./zenkoku.csv"
    with codecs.open(path, "r", "Shift-JIS", "replace") as file:
        j_cd = pd.read_table(file, delimiter=",")
        # a_cd = cd_list['市区町村CD']
        # ac_list = list(a_cd.unique().tolist())
    #print(conf)

    #prefecture = int(conf["prefecture"])
    df_1 = j_cd[j_cd['都道府県CD'] == prefecture]
    df_2 = df_1['市区町村CD']
    ac_list = list(df_2.unique().tolist())

    df_list = []
    tmp_list = []


    count = 0

    output_dir = "./tmp/code_{}/".format(prefecture)
    os.makedirs(output_dir, exist_ok=True)

    ac_restart_flg = True
    for gc in gc_list:
        #スキップ処理
        if conf["gc"] != "":
            if int(conf["gc"]) > int(gc):
                print("gc : {} skip".format(gc))
                continue

        if len(str(gc)) < 4:
            gc = "0" + str(gc)

        print("gc : {}".format(gc))
        for ac in tqdm(ac_list):
            area_count = 1
            if len(str(ac)) < 5:
                ac = "0" + str(ac)

            #スキップ処理
            if conf["ac"] != "":
                if conf["ac"] != ac and ac_restart_flg == True:
                    print("ac : {} skip".format(ac))
                    continue
                else:
                    ac_restart_flg = False
            else:
                ac_restart_flg = False
 
            if conf["start"] != "":
                start = int(conf["start"])
                print("restart : {}".format(start))
            else:
                start = 1

            #データ取得
            while(True):
#                print(start)
                file_name = "{}_{}_{}.csv".format(gc,ac,start)
                # 出力ファイルが存在したらスキップ
                if file_name in os.listdir(output_dir):
                    pass
                # 無かったら問い合わせて出力
                else:
                    time.sleep(0.5)
                    df =  getStoreInfos(str(gc),ac,start)
                    if df is not None :
                        df_list.append(df)
                        tmp_list.append(df)
                    else:
                        break
                    
    #                print(df)

                    count += 1
                    #if count % 10 == 0:
                    tmp_result = df #pd.concat(tmp_list)
                    #print(tmp_result)
                    with open(file_name,mode="w",encoding=conf["encode"],errors="ignore") as f:
                        tmp_result.to_csv(f,index=False)


                    log_df = pd.DataFrame({
                                "gc" :[gc],
                                "ac" :[ac],
                                "start" : [start]
                                })
                    with open("./log/log.csv".format(gc,ac,count),mode="w",encoding=conf["encode"],errors="ignore") as f:
                            log_df.to_csv(f)

                    #tmp_list = []

                    if len(df) < 100:
                        break
                
                start += 100
                area_count += 100
                
                #area_cd一つにつき上限が1万件
                if area_count > 10000:
                    area_count = 0
                    break

    #result = pd.concat(df_list)
    #print(result)
    #with open("hokkaido.csv",mode="w",encoding="cp932",errors="ignore") as f:
    #    result.to_csv(f)

if __name__ == "__main__":   
    with open("./conf.yaml") as f:
        conf = yaml.safe_load(f)
    print(conf)

    prefecture = conf["prefecture"]
    
    if prefecture == "all":
        prefecture_df = pd.read_csv("./prefecture_list.csv")
        prefecture_list = prefecture_df["Code"]
        for cd in prefecture_list:
            #print(cd)
            run(conf,int(cd))
    else:
        run(conf,int(prefecture))




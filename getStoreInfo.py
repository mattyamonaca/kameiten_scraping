import requests
import json
from urllib import parse
import pandas as pd

#appid = "dj00aiZpPU9lblRWbnBmYU9SOSZzPWNvbnN1bWVyc2VjcmV0Jng9ZTI-"

def getStoreInfos(gc,start):
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
        "ac" : "",
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
    

    response = requests.get(url)
    suffix = response.text.split("(")[0] + "("
    json_f = response.text.replace(suffix,"").rstrip(")")
    
    
    elements = json.loads(json_f) 

    print(len(elements["Feature"]))
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

        if "Station" in property.keys():
            station = element["Property"]["Station"][0]
            station_id_list.append(station["Id"])
            station_name_list.append(station["Name"])
            station_distance_list.append(station["Distance"])
            station_time_list.append(station["Time"])
        else:
            station_id_list.append(None)
            station_name_list.append(None)
            station_distance_list.append(None)
            station_time_list.append(None)

        if "Genre" in property.keys():
            genre = element["Property"]["Genre"][0]
            genre_code_list.append(genre["Code"])
            genre_name_list.append(genre["Name"])
        else:
            genre_code_list.append(genre)
            genre_name_list.append(genre)

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
        
if __name__ == "__main__":
    df =  getStoreInfos("01","1")
    print(df)
    df.to_csv("sample_output.csv")

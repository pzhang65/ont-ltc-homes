from src.GeoHubReq import GeoHubReq
from src.LTCScrapper import LTCScrapper
import pandas as pd
import csv
import os
import pandas

def print_df(dict):
    df = pd.DataFrame.from_dict(dict)
    print(df)

def write_csv(filename, fieldnames, dict):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='')
        writer.writeheader()
        for x in dict:
            writer.writerow(x)

def abs_path(filename):
    return os.path.join(os.getcwd(), "csv", f"{filename}.csv")

def merge_datasets(list1, list2):
    merged = []
    for i in range(len(list1)):
        new_dict = {**list1[i], **list2[i]}
        merged.append(new_dict)

    return merged

def write_merged(dataset, f):
    df = pandas.DataFrame.from_dict(dataset)
    # encoding windows-1252 for french accents
    # columns are in specific order. Used index location instead of actual str to save space
    df.to_csv("merged_LTC_homes.csv", ",", index=False, encoding='windows-1252', header=True,
            columns=[f[12], f[0], f[14], f[15], f[16], f[17], f[18],
                f[1], f[2], f[3], f[11], f[13], f[4], f[19],
                f[5], f[6], f[7], f[8], f[9], f[10]])


route = "https://services9.arcgis.com/a03W7iZ8T3s5vB7p/arcgis/rest/services/MOH_SERVICE_LOCATION/FeatureServer/0/query?where=SERV_TYPE%20%3D%20'LONG-TERM%20CARE%20HOME'&outFields=MOH_PRO_ID,SERV_DET,EN_NAME,ADDRESS_1,ADDRESS_2,COMMUNITY,POSTALCODE&outSR=4326&f=json"

res = GeoHubReq(route)
homes = res.get_homes()
## get list of MOH ids for use in LTCScrapper
ids = res.get_moh_id()

scrap = LTCScrapper()
ltc_dict = scrap.scrap_list(ids)

# Generate list of fields for use in generating merged csv
fields = scrap.get_keys()+res.get_keys()

merged = merge_datasets(ltc_dict, homes[:5])
write_merged(merged, fields)

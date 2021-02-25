from src.GeoHubReq import GeoHubReq
from src.LTCScrapper import LTCScrapper
import pandas as pd
import csv
import os

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

fieldnames = ['MOH_PRO_ID', 'SERV_DET','EN_NAME','ADDRESS_1','COMMUNITY',
            'POSTALCODE', 'ADDRESS_2', 'EFF_DATE']
route = "https://services9.arcgis.com/a03W7iZ8T3s5vB7p/arcgis/rest/services/MOH_SERVICE_LOCATION/FeatureServer/0/query?where=SERV_TYPE%20%3D%20%27LONG-TERM%20CARE%20HOME%27&outFields=MOH_PRO_ID,SERV_DET,EN_NAME,ADDRESS_1,COMMUNITY,POSTALCODE,ADDRESS_2,EFF_DATE&outSR=4326&f=json"

res = GeoHubReq(route)
res.get_response()

# get list of MOH ids for use in LTCScrapper
ids = res.get_moh_id()

scrap = LTCScrapper()
# take 10 entries as example
ltc_dict = scrap.scrap_list(ids[10:20])
write_csv(abs_path('scrapped_homes'), scrap.get_keys(), ltc_dict)

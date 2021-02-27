#/run.py
import csv
import os
import pandas
from src.GeoHubReq import GeoHubReq
from src.LTCScrapper import LTCScrapper

def print_df(data):
    """
    Print list of data to console as a panda dataframe for easy viewing
    """
    df = pd.DataFrame.from_dict(data)
    print(df)

def write_csv(filename, fieldnames, dict):
    """
    Write a list of dictionary (data) to a csv file
    """
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='')
        writer.writeheader()
        for x in dict:
            writer.writerow(x)

def abs_path(filename):
    """
    Given a filename, generates an absolute path for file saves
    """
    return os.path.join(os.getcwd(), "csv", f"{filename}.csv")

def merge_datasets(list1, list2):
    """
    Merges data retrieved from API and data from scrapped web reports
    """
    merged = []
    for i in range(len(list1)):
        new_dict = {**list1[i], **list2[i]}
        merged.append(new_dict)

    return merged

def write_merged(filename, dataset, f):
    """
    Create a dataframe from merged dataset to output in specific column order
    """
    df = pandas.DataFrame.from_dict(dataset)
    # encoding windows-1252 for french accents
    # columns are in specific order. Used index location instead of actual str to save space
    df.to_csv(filename, ",", index=False, encoding='windows-1252', header=True,
            columns=[f[12], f[0], f[14], f[15], f[16], f[17], f[18],
                f[1], f[2], f[3], f[11], f[13], f[4], f[19],
                f[5], f[6], f[7], f[8], f[9], f[10]])


# Route for accessing API, will improve later
route = "https://services9.arcgis.com/a03W7iZ8T3s5vB7p/arcgis/rest/services/MOH_SERVICE_LOCATION/FeatureServer/0/query?where=SERV_TYPE%20%3D%20'LONG-TERM%20CARE%20HOME'&outFields=MOH_PRO_ID,SERV_DET,EN_NAME,ADDRESS_1,ADDRESS_2,COMMUNITY,POSTALCODE&outSR=4326&f=json"

if __name__ == '__main__':
    res = GeoHubReq(route)
    homes = res.get_homes()
    # get list of MOH ids for use in LTCScrapper
    ids = res.get_moh_id()

    scrap = LTCScrapper()
    ltc_dict = scrap.scrap_list(ids)

    # Generate list of fields for use in generating merged csv
    fields = scrap.get_keys()+res.get_keys()

    merged = merge_datasets(ltc_dict, homes)
    write_merged(abs_path("merged_LTC_homes"), merged, fields)

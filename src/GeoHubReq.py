import requests
import csv
import pandas

class GeoHubReq:
    def __init__(self, route):
        self.route = route
        self.homes = []

    def get_response(self):
        data = []
        resp = requests.get(self.route).json()
        data += resp["features"]
        for row in data:
            self.homes.append(row['attributes'])

    def change_route(self, route):
        self.route = route

    def print_df(self):
        df = pandas.DataFrame.from_dict(self.homes)
        print(df)

    def get_moh_id(self):
        lst = []
        for x in self.homes:
            lst.append(x['MOH_PRO_ID'])
        return lst

    def write_csv(self, filename, fieldnames):
        with open(f'{filename}.csv', mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='')
            writer.writeheader()
            for x in self.homes:
                writer.writerow(x)



if __name__ == '__main__':
    fieldnames = ['MOH_PRO_ID', 'SERV_DET','EN_NAME','ADDRESS_1','COMMUNITY',
                'POSTALCODE', 'ADDRESS_2', 'EFF_DATE']
    route = "https://services9.arcgis.com/a03W7iZ8T3s5vB7p/arcgis/rest/services/MOH_SERVICE_LOCATION/FeatureServer/0/query?where=SERV_TYPE%20%3D%20%27LONG-TERM%20CARE%20HOME%27&outFields=MOH_PRO_ID,SERV_DET,EN_NAME,ADDRESS_1,COMMUNITY,POSTALCODE,ADDRESS_2,EFF_DATE&outSR=4326&f=json"
    res = GeoHubReq(route)
    lst = res.get_response()
    res.print_df()
    moh = res.get_moh_id()
    print(moh[:5])

#src/GeoHubReq.py
import requests

class GeoHubReq:
    def __init__(self, route):
        self.route = route
        self.homes = []
        self.keys = []

    def urban_or_rural(self, home):
        # 2nd char of Canadian postal code determines rural or urban
        if int(home['POSTALCODE'][1]) == 0: # 0 is rural
            return 'Rural'
        else: # all other numbers are urban
            return 'Urban'


    def get_homes(self):
        data = []
        resp = requests.get(self.route).json()
        data += resp["features"]#["attributes"]
        for row in data:
            home = row['attributes']
            # Determine if home is rural or urban
            home['Area Type'] = self.urban_or_rural(home)
            self.homes.append(home)

        return self.homes

    def get_keys(self):
        return list(self.homes[0].keys())

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

if __name__ == '__main__':
    route = "https://services9.arcgis.com/a03W7iZ8T3s5vB7p/arcgis/rest/services/MOH_SERVICE_LOCATION/FeatureServer/0/query?where=SERV_TYPE%20%3D%20%27LONG-TERM%20CARE%20HOME%27&outFields=MOH_PRO_ID,SERV_DET,EN_NAME,ADDRESS_1,COMMUNITY,POSTALCODE,ADDRESS_2,EFF_DATE&outSR=4326&f=json"
    res = GeoHubReq(route)
    lst = res.get_homes()
    fieldnames = res.get_keys()
    res.print_df()
    moh = res.get_moh_id()
    print(moh[:5])

import requests
from bs4 import BeautifulSoup

class LTCScrapper:
    route = "http://publicreporting.ltchomes.net/en-ca/homeprofile.aspx?Home="

    def __init__(self):
        self.homes = []
        self.keys = []

    def get_keys(self):
        return self.keys

    def scrap_one(self, id):
        # Get response from id
        resp = requests.get(self.route+str(id))
        # Generate soup object
        soup = BeautifulSoup(resp.content, 'html.parser')

        # Find all elements in main home profile element
        profile = soup.find(id='ctl00_ContentPlaceHolder1_divHomeProfile_item_Col1')

        # Find all elements in col1 and col2 for our key : value pairs
        col1 = profile.find_all(class_='Profilerow_col1')
        col2 = profile.find_all(class_='Profilerow_col2')

        # Get all texts from each element in col1 = keys, col2= values
        keys = []
        for x in col1:
            keys.append(x.get_text())
            
        # Set keys attribute as keys for use in generating csv
        self.keys = keys

        values = []
        for x in col2:
            values.append(x.get_text())

        # Return a dictionary with key:value pairs
        return dict(zip(keys, values))

    def scrap_list(self, list):
        for id in list:
            print(f'Scrapping home: {id}')
            # If nan try 0 before id !
            self.homes.append(self.scrap_one(id))
        return self.homes

    def print_df(self):
        df = pandas.DataFrame.from_dict(self.homes)
        print(df)

    def write_csv(self, filename, fieldnames):
        with open(f'{filename}.csv', mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='')
            writer.writeheader()
            for x in self.homes:
                writer.writerow(x)


if __name__ == '__main__':
    scrap = LTCScrapper()
    print(scrap.scrap_one(2872))

#src/LTCScrapper.py
import requests
from bs4 import BeautifulSoup

class LTCScrapper:
    route = "http://publicreporting.ltchomes.net/en-ca/homeprofile.aspx?Home="

    def __init__(self):
        self.homes = []
        self.keys = []

    def get_keys(self):
        return self.keys

    def scrap_phone(self, soup):
        """
        Returns only phone number
        """
        phone = soup.find(id='ctl00_ContentPlaceHolder1_divHomePhone')
        return phone.get_text().lstrip('Tel : ') # strip redundant chars


    def scrap_one(self, id):
        """
        Gets all required key value pairs from a page and returns a dictionary of data
        Also checks for some ID discrepencies
        """
        # Get response from id
        resp = requests.get(self.route+str(id))
        # Generate soup object
        soup = BeautifulSoup(resp.content, 'html.parser')

        # Get phone from another div element first for use later
        phone = self.scrap_phone(soup)

        # check if home id was invalid
        # invalid id returns the same page just without info
        if phone == '':
            #  try 0 before id
            resp = requests.get(self.route+str(0)+str(id))
            # re-grab everything
            soup = BeautifulSoup(resp.content, 'html.parser')
            phone = self.scrap_phone(soup)

        # Find all elements in main home profile element
        profile = soup.find(id='ctl00_ContentPlaceHolder1_divHomeProfile_item_Col1')

        # Find all elements in col1 and col2 for our key : value pairs
        col1 = profile.find_all(class_='Profilerow_col1')
        col2 = profile.find_all(class_='Profilerow_col2')

        # Get all texts from each element in col1 = keys, col2= values
        keys = []
        for i, x in enumerate(col1):
            # skip 2nd column
            if i not in (1,5):
                keys.append(x.get_text())

        values = []
        for i, x in enumerate(col2):
            # skip 2nd column
            if i not in (1,5):
                values.append(x.get_text())

        keys.append('Telephone')
        # Set keys attribute as keys for use in generating csv

        self.keys = keys
        values.append(phone)
        # Return a dictionary with key:value pairs
        return dict(zip(keys, values))

    def scrap_list(self, list):
        """
        Scraps all homes from a list of home IDs
        """
        for id in list:
            print(f'Scrapping home: {id}')
            # If nan try 0 before id !
            self.homes.append(self.scrap_one(id))
        return self.homes

if __name__ == '__main__':
    scrap = LTCScrapper()
    print(scrap.scrap_one(2872))

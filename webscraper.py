from pickle import TRUE
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd
import numpy as np
import re

chrome_options = webdriver.ChromeOptions()
chromedriver_path = "/Users/michaelyfu/Documents/Coding/chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver_path)

class Webscraping:
    def __init__(self):
        # self.properties = {} # follow this format: {location: {listing: [total cost, rating, num_of_ratings, etc.]}}
        self.properties = {} # follow this format: {listing: [location, total cost, rating, num_of_ratings, etc.]}}
        self.DRIVER_ON = TRUE

    def start_search(self, date_start, date_end, num_adults, max_price, search_num):
        #search_num is currently a temporary fix to a bug where locations have the same name
        # input start, end dates as Y-m-d (ex. 2022-06-13) format
        locations = {
            # 'Maine': f"https://www.airbnb.com/s/Maine--United-States/homes?adults={num_adults}&place_id=ChIJ1YpTHd4dsEwR0KggZ2_MedY&refinement_paths%5B%5D=%2Fhomes&checkin={date_start}&checkout={date_end}&tab_id=home_tab&query=Maine%2C%20United%20States&flexible_trip_lengths%5B%5D=one_week&price_max={max_price}&search_type=filter_change",
            'Seattle': f"https://www.airbnb.com/s/Downtown-Seattle--Seattle--WA/homes?adults={num_adults}&place_id=ChIJLVcisbZqkFQRQx2ONFFfxkw&refinement_paths%5B%5D=%2Fhomes&checkin={date_start}&checkout={date_end}&tab_id=home_tab&query=Downtown%20Seattle%2C%20Seattle%2C%20WA&flexible_trip_lengths%5B%5D=one_week&price_max={max_price}&search_type=filter_change",
            # 'New Hampshire': f"https://www.airbnb.com/s/New-Hampshire--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=may&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&query=New%20Hampshire%2C%20United%20States&place_id=ChIJ66bAnUtEs0wR64CmJa8CyNc&checkin={date_start}&checkout={date_end}&adults={num_adults}&source=structured_search_input_header&search_type=autocomplete_clicktype=filter_change&price_max={max_price}",
        }
        # self.properties = dict.fromkeys(locations, {})

        for location in locations:
            driver.get(locations[location])
            page = requests.get(locations[location], headers = {'User-agent': 'Super Bot Power Level Over 9000'})
            soup = BeautifulSoup(page.content, 'html.parser')
            soup.prettify()
            listings = soup.find_all("div", {"itemprop": "itemListElement"})

            parse_rules = {"name": ["t1jojoys dir dir-ltr", "</div>", ".*>"], "total_cost": ["_tt122m", "</span></div>", ".*>"]}
            # parse_rules not used at the moment; am planning on simplifying code in lines 43-67 into a lambda function that can filter over parse_rules

            for listing in listings:
                name = listing.find("div", {"class": "t1jojoys dir dir-ltr"}).getText()
                # name = name.replace("</div>", "")
                # name = re.sub(".*>", "", name)
                if name in self.properties:
                    name += " " + str(search_num)

                total_cost = listing.find("div", {"class": "_tt122m"}).getText()
                # print(total_cost)
                # total_cost = str(listing.find("div", {"class": "_tt122m"}))
                # total_cost = total_cost.replace("</span></div>", "")
                # total_cost = re.sub(".*>", "", total_cost)

                self.properties[name] = []
                self.properties[name].append(location)
                self.properties[name].append(total_cost)

                # beds_bedrooms = str(listing.find("div", {"class": "f15liw5s s1cjsi4j dir dir-ltr"}))
                beds_bedrooms = listing.find("div", {"class": "f15liw5s s1cjsi4j dir dir-ltr"}).getText()
                num_beds = re.search('\d+\sbed[s]?', beds_bedrooms).group(0)
                try:
                    num_bedrooms = re.search('\d+\sbedroom[s]?', beds_bedrooms).group(0)
                except (TypeError, AttributeError):
                    num_bedrooms = "N/A"
                search_num += 1
                # time.sleep(1)
        df = pd.DataFrame.from_dict(self.properties, orient = 'Index', columns = ["Total Cost", "Location"])
        df.index.name = 'Property Name'
        df.reset_index(inplace=True)
        print(df)
        df.to_csv('file_name.csv')
    
    def get_listings(self, url):
        pass

    def scrape_page(self):
        pass

def main():
    webscraper = Webscraping()
    webscraper.start_search('2022-06-14', '2022-06-17', '4', '300', 0)
    print('length:', len(webscraper.properties))

if __name__ == '__main__':
    main()

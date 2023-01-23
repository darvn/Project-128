from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

browser = webdriver.Chrome("chromedriver.exe") 
browser.get(START_URL)

time.sleep(10)

scraped_data = []

def scrape(hyperlink):

    page = requests.get(hyperlink)

    soup = BeautifulSoup(browser.page_source, "html.parser")

    tables = soup.find_all("table", attrs={"class", "wikitable"})

    temp_list = []

    table_body = tables.find_all("tbody")

    table_rows = table_body.find_all("tr")
           
    

    for row in table_rows:
        table_cols = row.find_all('td')
        print(table_cols)

        for col_data in table_cols:
            #print(col_data.text)
            data = col_data.text.strip()
            #print(data)
            temp_list.append(data)

   

    scraped_data.append(temp_list)

scrape()

dwarf_data = []

for i in range(0, len(scraped_data)):
    Stars_names = scraped_data[i][1]
    Distance = scraped_data[i][3]
    Mass = scraped_data[i][5]
    Radius = scraped_data[i][6]
    required_data = [Stars_names, Distance, Mass, Radius]
    dwarf_data.append(required_data)


headers = ["Star_name", "Distance", "Mass", "Radius"]

star_df_1 = pd.DataFrame(dwarf_data, columns=headers)

star_df_1.to_csv('scraped_data.csv',index=True, index_label="id")

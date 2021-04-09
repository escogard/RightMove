import pandas as pd
from bs4 import BeautifulSoup
import requests
import nltk
from nltk import WordNetLemmatizer
from datetime import datetime, timedelta, date
import re
from tqdm import tqdm

###### Dates ####
today = date.today().strftime('%Y%m%d')
yesterday = (date.today() - timedelta(days=1)).strftime('%Y%m%d')
print("Today is : ", today)

def rms_buy(borough,location, min_rooms=1, max_rooms=6):
    '''Takes a borough name and a right move user defined location. Recommend to use dict'''
    # Get initial page
    base_url = f"https://www.rightmove.co.uk/property-for-sale/find.html?maxBedrooms={max_rooms}&minBedrooms={min_rooms}&sortType=6&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords=&"
    base_url += location
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #concatenate all pages into single df
    big_df = pd.DataFrame()
    listings_html = soup.find_all('span',class_='searchHeader-resultCount')
    listings_n = int(listings_html[0].get_text())
    print(listings_n)
    ##### Get all listing from search in every row
    for page in tqdm(range(0,listings_n, 24)): #24 is the number of listings per page
        #scraping each page
        print(page)
        base_url = "https://www.rightmove.co.uk/property-for-sale/find.html?maxBedrooms=3&minBedrooms=2&sortType=6&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords=&"
        base_url += location
        idx_page = '&index=' + str(page)
        base_url += idx_page
        
        page = requests.get(base_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        listings_div = soup.find_all(class_="l-searchResult is-list")
        
        RM_id = [tag.get('id')[9:] for tag in listings_div]
        
        record_id = [date.today().strftime('%Y%m%d')+ids_ind for ids_ind in RM_id]
        
        prop_url = ["https://www.rightmove.co.uk/properties/" + id_iter for id_iter in RM_id]

        prop_price = [re.sub(r'\D',"",prices.text) for prices in soup.find_all(class_="propertyCard-priceValue")]
        room_n = [re.sub(r'\D',"",rooms.text) for rooms in soup.find_all(class_="propertyCard-title")]
        
        status_all = [status.text.split() for status in soup.find_all(class_="propertyCard-branchSummary-addedOrReduced")]
        status = []
        for n in status_all:
            if "Added" in n:
                status.append('Added')
            elif "Reduced" in n:
                status.append('Reduced')
            else:
                status.append('na')
         
        status_date = []
        for n in status_all:
            if "today" in n:
                status_date.append(date.today())

            elif "yesterday" in n:
                status_date.append(date.today() - timedelta(days=1))

            elif len(n) == 3:
                status_date.append(datetime.strptime(n[2], '%d/%m/%Y').date())

            else:
                status_date.append('-')

        
        outside = []
        lemma = WordNetLemmatizer()
        for line in [n.text for n in soup.find_all(itemprop="description")]:
            tokens = nltk.word_tokenize(line.lower())
            lem_tokens = list(map(lemma.lemmatize, tokens))
            if "communal" in lem_tokens:
                outside.append('communal')
            elif "garden" in lem_tokens:
                outside.append('garden')
            elif "terrace" in lem_tokens:
                outside.append('terrace')
            elif "balcony" in lem_tokens:
                outside.append('balcony')
            elif "balconies," in lem_tokens:
                outside.append('balcony')
            elif "patio" in lem_tokens:
                outside.append('patio')
            else:
                outside.append('-')
        
        df = pd.DataFrame(list(zip(record_id, RM_id, prop_url, prop_price, room_n, status,status_date,outside)),\
                          columns = ['record_id','RM_id', 'prop_url','price','rooms','status','status_date','outside'])
        
        big_df = big_df.append(df, ignore_index=True)

    return big_df






def rms_rent(borough,location, min_rooms=1, max_rooms=6):
    # Get initial page
    print(borough)
    base_url = f"https://www.rightmove.co.uk/property-to-rent/find.html?minBedrooms={min_rooms}&maxBedrooms={max_rooms}&keywords=&sortType=6&viewType=LIST&channel=RENT&index=0&radius=0.0&"
    base_url += location
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #concatenate all pages into single df
    big_df = pd.DataFrame()
    listings_html = soup.find_all('span',class_='searchHeader-resultCount')
    listings_n = int(listings_html[0].get_text())

    ##### Get all listing from search in every row
    for page in tqdm(range(0,listings_n, 24)): #24 is the number of listings per page
        #scraping each page
        #print(page)
        base_url = "https://www.rightmove.co.uk/property-to-rent/find.html?minBedrooms=2&maxBedrooms=3&keywords=&sortType=6&viewType=LIST&channel=RENT&radius=0.0&"
        base_url += location
        idx_page = '&index=' + str(page)
        base_url += idx_page
        
        page = requests.get(base_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        listings_div = soup.find_all(class_="l-searchResult is-list")
        
        RM_id = [tag.get('id')[9:] for tag in listings_div]
        
        record_id = [date.today().strftime('%Y%m%d')+ids_ind for ids_ind in RM_id]
        
        prop_url = ["https://www.rightmove.co.uk/property-to-rent/property-" + id_iter + ".html" for id_iter in RM_id]

        prop_price = [re.sub(r'\D',"",prices.text) for prices in soup.find_all(class_="propertyCard-priceValue")]
        room_n = [re.sub(r'\D',"",rooms.text) for rooms in soup.find_all(class_="propertyCard-title")]
        
        status_all = [status.text.split() for status in soup.find_all(class_="propertyCard-branchSummary-addedOrReduced")]
        status = []
        for n in status_all:
            if "Added" in n:
                status.append('Added')
            elif "Reduced" in n:
                status.append('Reduced')
            else:
                status.append('na')
         
        status_date = []
        for n in status_all:
            if "today" in n:
                status_date.append(date.today())

            elif "yesterday" in n:
                status_date.append(date.today() - timedelta(days=1))

            elif len(n) == 3:
                status_date.append(datetime.strptime(n[2], '%d/%m/%Y').date())

            else:
                status_date.append('-')

        
        outside = []
        lemma = WordNetLemmatizer()
        for line in [n.text for n in soup.find_all(itemprop="description")]:
            tokens = nltk.word_tokenize(line.lower())
            lem_tokens = list(map(lemma.lemmatize, tokens))
            if "communal" in lem_tokens:
                outside.append('communal')
            elif "garden" in lem_tokens:
                outside.append('garden')
            elif "terrace" in lem_tokens:
                outside.append('terrace')
            elif "balcony" in lem_tokens:
                outside.append('balcony')
            elif "balconies," in lem_tokens:
                outside.append('balcony')
            elif "patio" in lem_tokens:
                outside.append('patio')
            else:
                outside.append('-')
        
        df = pd.DataFrame(list(zip(record_id, RM_id, prop_url, prop_price, room_n, status,status_date,outside)),\
                          columns = ['record_id','RM_id', 'prop_url','price','rooms','status','status_date','outside'])
        
        big_df = big_df.append(df, ignore_index=True)

    return big_df


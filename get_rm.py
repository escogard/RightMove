from RM_scrapper import rms_buy, rms_rent
from locations_dict import boroughs
from datetime import date

today = date.today().strftime('%Y%m%d')

for borough, loc in boroughs.items():
    listing_buy = rms_buy(borough,loc)
    listing_rent = rms_buy(borough,loc)
    listing_buy.to_excel("data/buy/" + today + "RM_buy_" + borough + ".xlsx", index = False)
    listing_rent.to_excel("data/rent/" + today + "RM_rent_" + borough + ".xlsx", index = False)
    
    

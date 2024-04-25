from scrapejaya import *
from scrapevgw import *
from scrapelotus import *
from scrapeaeon import *
import pyrebase


config = {
    "apiKey": "AIzaSyCvrfjVrBgcobvJgYcE_Yda7OrN3xbBhoQ",
    "authDomain": "pricescrape2.firebaseapp.com",
    "projectId": "pricescrape2",
    "databaseURL": "https://pricescrape2-default-rtdb.firebaseio.com/",
    "storageBucket": "pricescrape2.appspot.com",
    "messagingSenderId": "83119362702",
    "appId": "1:83119362702:web:b89a01e53e3dbd3f202fdf",
    "measurementId": "G-Z27T8MYY96"
}


if __name__ == '__main__':
    firebase = pyrebase.initialize_app(config)
    database = firebase.database()
    shared_results = []

    urlj = "https://jggp.jayagrocer.com/collections/fruits"
    urlj2 = "https://jggp.jayagrocer.com/collections/vegetables"

    selectorsj = {
        "product_name": '.product-list.product-list--collection .product-item__title.text--strong.link',
        "price": '.product-list.product-list--collection .price',
    }
    # result = start_scraping_jaya(urlj, urlj2, selectorsj)

    # database.child("jaya grocer").set(result)

    # Scrape lotus
    urll = "https://www.lotuss.com.my/en/category/fresh-produce/fruits?sort=relevance:DESC"
    urll2 = "https://www.lotuss.com.my/en/category/fresh-produce/vegetables?sort=relevance:DESC"
    #https://www.lotuss.com.my/en/category/fresh-produce/fruits?sort=relevance:DESC
    selectorsl = {
        "product_name": 'product-title',
        "price": 'GCRGw',
    }
    # result = start_scraping_lotus(urll,urll2, selectorsl)
    # database.child("lotus").set(result)

    urlvgw = "https://vgw.bites.com.my/collections/fruits"
    urlvgw2 = "https://vgw.bites.com.my/collections/vegetables"
    selectorsv = {
        "product_name": 'cd chp selectorgadget_suggested',
        "price": 'GCRGw',
    }
    # result = start_scraping_vgw(urlvgw,urlvgw2, selectorsv)
    # database.child("village grocer").set(result)

    url3 = "https://myaeon2go.com/products/category/7644592/fruits"

    selectors3 = {
        "product_name": "nhQRizN1GA1WpbpCy_qn g-brand-text",
        "price": '//*[@id="__layout"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/div/span[1]',
    }
    results3 = start_scraping_aeon(url3, selectors3)

    print("success")


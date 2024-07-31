import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import logging

logging.basicConfig(filename="scrapper.log", level=logging.INFO)

def connect_mongo():
    client = pymongo.MongoClient("mongodb+srv://wokenupshashank:<Meena@2316>@cluster0.s2uvunb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["ecommerce"]
    collection = db["products"]
    return collection

def scrape_flipkart(search_query):
    try:
        flipkart_url = "https://www.flipkart.com/search?q=" + search_query
        response = requests.get(flipkart_url)
        flipkart_html = bs(response.content, "html.parser")
        
        products = []
        bigboxes = flipkart_html.findAll("div", {"class": "cPHDOP col-12-12"})
        for box in bigboxes:
            title = box.find("a", {"class": "IRpwTa"}).get_text() if box.find("a", {"class": "IRpwTa"}) else None
            price = box.find("div", {"class": "_30jeq3"}).get_text() if box.find("div", {"class": "_30jeq3"}) else None
            rating = box.find("div", {"class": "_3LWZlK"}).get_text() if box.find("div", {"class": "_3LWZlK"}) else None
            description = box.find("div", {"class": "_1xgFaf"}).get_text() if box.find("div", {"class": "_1xgFaf"}) else None

            if title and price:
                products.append({
                    'Title': title,
                    'Price': price,
                    'Rating': rating if rating else 'N/A',
                    'Description': description if description else 'No Description'
                })

        collection = connect_mongo()
        collection.insert_many(products)
        logging.info(f"Inserted {len(products)} records into MongoDB")
        return products
    except Exception as e:
        logging.error(f"Error in scrape_flipkart: {e}")
        return []

if __name__ == '__main__':
    # This block is for testing purposes and should be removed or commented out in production.
    search_query = 'iphone11'
    products = scrape_flipkart(search_query)
    print(products)

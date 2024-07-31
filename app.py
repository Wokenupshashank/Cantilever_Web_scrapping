from flask import Flask, render_template, request
from pymongo import MongoClient
from scrape_flipkart import scrape_flipkart

app = Flask(__name__)

def connect_mongo():
    client = pymongo.MongoClient("mongodb+srv://wokenupshashank:<Meena@2316>@cluster0.s2uvunb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["ecommerce"]
    collection = db["products"]
    return collection

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        try:
            search_query = request.form['query']
            collection = connect_mongo()

            # Check if the products are already scraped and stored in MongoDB
            if collection.count_documents({"Title": {"$regex": search_query, "$options": "i"}}) == 0:
                scrape_flipkart(search_query)
            results = list(collection.find({"Title": {"$regex": search_query, "$options": "i"}}))
            return render_template('results.html', query=search_query, results=results)
        except Exception as e:
            return str(e)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

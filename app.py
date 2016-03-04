from flask import Flask
import requests
import json
app = Flask(__name__)

@app.route("/")
def crawl():
    diseaseList = [
    'alzheimers',
    'hiv'
    ]

    def cttv(diseaseName):
        r =  requests.get('https://www.targetvalidation.org/api/latest/search?size=99999&from=0&q='+diseaseName)
        print r.json()

    map(cttv,diseaseList)

    return "hello"

if __name__ == "__main__":
    app.run(debug=True)

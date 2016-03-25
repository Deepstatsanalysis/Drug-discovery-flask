from flask import Flask,make_response,jsonify,request
from flask.ext.elasticsearch import FlaskElasticsearch
import requests
import json
import scrapy
# from multiprocessing import Pool
from processing import Pool
app = Flask(__name__)

#we are using default elasticsearch address
#i.e. http://localhost:9200/
es = FlaskElasticsearch(app)


@app.after_request
def add_cors_headers(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Credentials', 'true')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
	response.headers.add('Access-Control-Allow-Headers', 'Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET')
	response.headers.add('Access-Control-Allow-Methods', 'POST')
	response.headers.add('Access-Control-Allow-Methods', 'PUT')
	response.headers.add('Access-Control-Allow-Methods', 'DELETE')
	return response


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


@app.route("/diseases/names",methods=['GET'])
def get_diseases():
	k = es.search(index="diseases", doc_type='ypq' ,body='{ "query": { "match_all": {} }, "fields" : ["name","code"] }')['hits']
	return make_response(jsonify({'data': k }), 200)


@app.route("/")
def get_data():
    k = es.search(index="diseases",body='{ "query": { "match_all": {} } }')
    return make_response(jsonify({'data': k }), 200)

@app.route("/crawl", methods=['POST'] )
def crawl():
	code = request.json['code']
	s = es.search(index="diseases",doc_type="ypq", body='{ "query": { "query_string": {"query":"'+code+'","fields":["code"]} } }')
	if s['hits']['total']:
		return "data alredy present"
	else:
		d = requests.get("https://www.targetvalidation.org/api/latest/association?disease="+code+"&datastructure=flat&stringency=1&filterbyscorevalue_min=0")

		if d.json()['total'] == 0:
			return "No records found"
		else:
			targetSymbols = []

			for i in d.json()["data"]:
				x = {}
				x["symbol"] =i["target"]["symbol"]
				x["id"] = i["target"]["id"]

				k = requests.get("https://www.targetvalidation.org/api/latest/association?target="+x["id"])
				diseases = []
				for m in k.json()["data"]:
					diseases.append(m["disease"]["name"])
				x["disease"] = diseases
				targetSymbols.append(x)

			payload = {
				"name":d.json()["data"][0]["disease"]["name"],
				"code":code,
				"data":d.json()["data"],
				"datatypes":d.json()["available_datatypes"],
				"facets":d.json()["facets"]["datatypes"],
				"targetSymbols":targetSymbols
			}
			# p = es.create(index="diseases",doc_type="ypq",body=json.dumps(payload))

		return json.dumps(payload)


@app.route("/diseases/selected", methods=['POST'])
def get_selected_data():

	values = request.json["selected_values"]

	diseasesNames = []

	for i in values:
		diseasesNames.append(i['fields']['name'][0])
	query_builder = {
				"query" : {
			        "filtered" : {
			            "filter" : {
			                "terms" : {
			                    "name" : diseasesNames
			                }
			            }
			        }
			    },
				"_source" : ["name","data","datatypes","facets","targetSymbols"]
			}


	s = es.search(index="diseases",doc_type="ypq", body=json.dumps(query_builder))

	return json.dumps(s)


@app.route("/diseases/datatypes", methods=['POST'])
def get_selected_datatypes():

	selected_datatypes = request.json["selected_datatypes"]
	selected_diseases = request.json["selected_diseases"]
	diseasesNames = []
	datatypes = []

	for i in selected_diseases:
		diseasesNames.append(i['fields']['name'][0])

	for i in selected_datatypes:
		datatypes.append(i)


	query_builder = {
				  "query": {
				    "has_parent": {
				      "data": "data",
				      "query": {
				        "match": {
				          "association_score": 1
				        }
				      }
				    }
				  },
		"_source" : ["name","data","datatypes"]
	}



	s = es.search(index="diseases",doc_type="ypq", body=json.dumps(query_builder))
	print diseasesNames

	print datatypes

	return json.dumps(s)



if __name__ == "__main__":
    app.run(debug=True)

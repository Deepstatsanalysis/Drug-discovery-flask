from flask import Flask,make_response,jsonify
from flask.ext.elasticsearch import FlaskElasticsearch
import requests
import json
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


@app.route("/diseases/names")
def get_diseases():
    k = es.search(index="diseases", doc_type='names' ,body='{ "query": { "match_all": {} } }')['hits']
    print json.dumps(k)
    return make_response(jsonify({'data': k }), 200)


@app.route("/")
def get_data():
    k = es.search(index="diseases",body='{ "query": { "match_all": {} } }')['hits']['hits'][0]['_source']
    print json.dumps(k)
    return make_response(jsonify({'data': k }), 200)



# @app.route("/crawl")
# def crawl():
#
#     return_data = {}
#     nodes = list(set())
#     links = []
#
#     diseaseList = [
#         {'diseaseName':'asthma','code':'EFO_0000270'},
#         # {'diseaseName':'hiv','code':'EFO_0000764'}
#     ]
#     def cttv(obj):
#         do = {}
#         do["Name"] = obj["diseaseName"]
#         do["Id"] = obj["code"]
#         nodes.append(do)
#
#         d = requests.get("https://www.targetvalidation.org/api/latest/association?disease="+obj['code']+"&datastructure=flat&stringency=1&filterbyscorevalue_min=0")
#
#         for i in d.json()['data']:
#             node_obj = {}
#             link_obj = {}
#
#             node_obj["Name"] = i["target"]["name"]
#             node_obj["Id"] = i["target"]["symbol"]
#             nodes.append(node_obj)
#
#             link_obj["Source"] = i["target"]["symbol"]
#             link_obj["Target"] = obj["code"]
#             link_obj["Value"] = 1
#             links.append(link_obj)
#
#     map(cttv,diseaseList)
#
# 	return_data["Nodes"] = nodes
#     return_data["Links"] = links
#
#     return json.dumps(p.content, default = set_default)

if __name__ == "__main__":
    app.run(debug=True)

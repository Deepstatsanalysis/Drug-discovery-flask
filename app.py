from flask import Flask,make_response,jsonify,request
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
    k = es.search(index="diseases", doc_type='ypq' ,body='{ "query": { "match_all": {} }, "fields" : ["name","code"] }')['hits']
    print json.dumps(k)
    return make_response(jsonify({'data': k }), 200)


@app.route("/")
def get_data():
    k = es.search(index="diseases",body='{ "query": { "match_all": {} } }')
    print json.dumps(k)
    return make_response(jsonify({'data': k }), 200)

@app.route("/crawl", methods=['POST'])
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
			payload = {
				"name":d.json()["data"][0]["disease"]["name"],
				"code":code,
				"data":d.json()["data"]
			}
			p = es.create(index="diseases",doc_type="ypq",body=json.dumps(payload))

			return "Data successfully crawled"


@app.route("/diseases/selected", methods=['POST'])
def get_selected_data():

	values = request.json["selected_values"]

	diseasesNames = []

	for i in values:
		diseasesNames.append(i['fields']['name'][0])

	print "###########################"
	print diseasesNames
	print "###########################"

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
				"_source" : ["name","data"]
			}


	s = es.search(index="diseases",doc_type="ypq", body=json.dumps(query_builder))

	print json.dumps(s)

	return json.dumps(s)





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

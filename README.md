# GSoC 2016 Prototype for BioJS.
## Project : Visualization of target-disease relationship in drug discovery
This is backend end module which has been developed using Python Flask.

## Pre-requirements
Elasticsearch server on port 9200

## Setup:
1. clone the repository `git clone https://github.com/ayusharma/Drug-discovery-flask.git`
2. Create virtualenv : `virtualenv venv`
3. Activate virtualenv: `source venv/bin/activate`
4.  install requirements using `pip install -r  requirement.txt`
5. Setup elastic search server.
6. Create an index with name `diseases`.


## Elastic Mapping
Make POST call on URL: `http://localhost:9200/diseases/ypq/_mapping`
```javascript
{
  "properties": {
    "data": {
      "type": "object",
      "properties": {
       "association_score":{"type":"long"},
        "datatypes": {
          "type": "object",
          "properties": {
          "association_score":{"type":"long"},
            "datasources": {
              "type": "object",
              "properties": {
                "association_score": {
                  "type": "string"
                }
              }
            }
          }
        }
      }
    },
    "name": {
      "type":"string",
      "index":"not_analyzed"
    }
  }
}
```
## Run
`python app.py`

## Contributing

All contributions are welcome.

## Support

If you have any problem or suggestion please open an issue [here](https://github.com/ayusharma/Drug-discovery-flask/issues).

## License

The MIT License

Copyright (c) 2016, ayushsharma

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

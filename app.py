from flask import Flask, jsonify, request
import json
import os
import time
from flask_pymongo import PyMongo
from flask_cors import CORS
import dns
import pymongo


# create the app

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://maizie:qwertyuiop123@gene.njw4a.mongodb.net/Gene?retryWrites=true&w=majority"
CORS(app)
mongo = PyMongo(app)

# 新加的
@app.route('/')
def index():
    # return app.send_static_file('index.html')
    return jsonify({"response": "this is the first page"})


@app.route('/home')
def say_hello_world():
    collection = mongo.db.papers
    papers = collection.find().sort('_id').limit(400)
    output = []
    key = 0

    for i in papers:
        output.append({'title' : i['Title'], 
                       'pmc_id': i['PMCid'], 
                       'date': i['Title'].split(' ')[-1][:-1], 
                       'key': key, 
                       'gene_type': i['gene_type'][-5:], 
                       'sentences': i['Sentences']})
        key = key + 1
    return jsonify({'result': output})




@app.route('/api/', methods=['POST', 'GET'])
def api_post():
    if request.method == 'POST':
        collection = mongo.db.papers
        req = request.json
        out = []
        result = collection.find({"$or": [{"PMCid": {"$regex": req}}, {"Title": {"$regex": req}}, {"gene_type"[0]: {"$regex": req}}]})
        key = 0
        
        for i in result:
            out.append({'title' : i['Title'], 'pmc_id': i['PMCid'], 
                        'date': i['Title'].split(' ')[-1][:-1],  
                        'key': key, 
                        'gene_type': i['gene_type'][-5:], 'sentences': i['Sentences']})
            key = key + 1
        
        return jsonify({'result': out})
        
@app.route('/searchGene/', methods=['POST', 'GET'])
def search_gene():
    if request.method == 'POST':
        gene_list = mongo.db.genes
        req = request.json
        out = []
        result = gene_list.find_one({"Gene name": {"$regex": req}})

        # out.append({'name' : result['Gene name'], 'type': result['Gene sfari class'], 'summary': result['Summary']})
        
        return jsonify({'name' : result['Gene name'], 
                        'type': result['Gene sfari class'], 
                        'related_npmi': result['Related phenotype NPMI'],
                        'paper_num': result['Summary']['Paper number'],
                        'sentence_num': result['Summary']['Sentence number']
                        })

# @app.errorhandler(404)
# def not_found(e):
#     return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()

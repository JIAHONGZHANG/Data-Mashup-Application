from flask import Flask, jsonify, request, Response
from flask_restful import reqparse
import requests
import os
import pandas as pd
import pymongo
import json
import random
import re

app = Flask(__name__)

mng_client = pymongo.MongoClient(host='mongodb://LlZzYy:LlZzYy@ds231090.mlab.com:31090/project')
mng_db = mng_client['project']

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
state_dict = {v:k for k,v in states.items()}

def get_post_args(arg_names, arg_types):
    parser = reqparse.RequestParser()
    for i in range(len(arg_names)):
        parser.add_argument(arg_names[i], type=arg_types[i])
    return parser.parse_args()

@app.route("/search", methods=['GET'])
def search():
    args = get_post_args(['year'], [str])
    year = args.get('year')
    query = {"date": {'$regex': year}}
    db_cm = mng_db['detailed_gunshot']
#    r = requests.get("http://localhost:5000/gun_shot/detailed_gunshot", json=query, headers = {'Content-Type':'application/json'})
    r = db_cm.find(query, {"_id":1, "date":1, 'state':1, 'n_injured':1, 'n_killed':1})
    result = []
    for doc in r:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    # print(result)

    return jsonify(result), 200

@app.route("/graph", methods=['GET'])
def graph():
    args = get_post_args(['year'], [str])
    year = args.get('year')
    query = {"date": {'$regex': year}}
    db_cm = mng_db['detailed_gunshot']
#    r = requests.get("http://localhost:5000/gun_shot/detailed_gunshot", json=query, headers = {'Content-Type':'application/json'})
    r = db_cm.find(query, {"date":1, 'state':1})
    result = []
    for doc in r:

        doc['_id'] = str(doc['_id'])
        result.append(doc)
    # print(result)
    state_count = {k:0 for k in state_dict.keys()}
    for record in result:
        print(record)
        state_count[record['state']] = state_count[record['state']] + 1
    json_response = []
    for state,count in state_count.items():
        s_c = {}
        s_c['state'] = state
        s_c['count'] = count
        json_response.append(s_c)
    return jsonify(json_response), 200

@app.route("/news", methods=['GET'])
def news():
    RANDOM_TOKEN = 5
    args = get_post_args(['year'], [str])
    year = args.get('year')
    query = {'date': {'$regex': year}}
    db_cm = mng_db['detailed_gunshot']
    r = db_cm.find(query, {"date":1, 'state':1, 'source_url':1})
    result = []
    for doc in r:
        doc['_id'] = str(doc['_id'])
        result.append(doc)

    url='http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/'
    title = 'urlTitle'
    slice = random.sample(result, RANDOM_TOKEN)
    print(slice)
    response = []
    for line in slice:
        try:
            r_d = {}
            source_url = line['source_url']
            news_title = requests.post(url+title, data={'url': source_url}).text
            rr = re.findall(r"(?=>).*(?=</span>&nbsp)", news_title)
            t = rr[0][1:]
            r_d['title'] = t
            r_d['url'] = source_url
            response.append(r_d)

        except:
            continue
    return jsonify(response), 200




app.run(port=5001)
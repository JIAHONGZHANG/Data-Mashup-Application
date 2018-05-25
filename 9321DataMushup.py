from flask import Flask, render_template, jsonify
from data_process import *
import json
import random
import re

app = Flask(__name__)
mng_client = pymongo.MongoClient(host='mongodb://LlZzYy:LlZzYy@ds231090.mlab.com:31090/project')
mng_db = mng_client['project']


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/graph?area=<area>&timefrom=<timefrom>&timeto=<timeto>', methods=['GET'])
def search_by_no_case(area, timefrom, timeto):
    if not area:
        return jsonify(Message='Please input the valid state name.'), 400

    elif not timefrom or not timeto:
        return jsonify(Message='Please specify the start time or end time.'), 400
    return jsonify(query_by_no_case(area, timefrom, timeto)), 200

@app.route('/search?area=<area>&timefrom=<timefrom>&timeto=<timeto>', methods=['GET'])
def search_by_period(area, timefrom, timeto):
    if not area:
        return jsonify(Message='Please input the valid state name.'), 400

    elif not timefrom or not timeto:
        return jsonify(Message='Please specify the start time or end time.'), 400

    return jsonify(query_by_period(area, timefrom, timeto)), 200

@app.route('/population')
def population_page():
    return '<script type=\'text/javascript\' src=\'http://dataviz.worldbank.org/javascripts/api/viz_v1.js\'></script><div class=\'tableauPlaceholder\' style=\'width: 1080px; height: 1067px;\'><object class=\'tableauViz\' width=\'1080\' height=\'1067\' style=\'display:none;\'><param name=\'host_url\' value=\'http%3A%2F%2Fdataviz.worldbank.org%2F\' /> <param name=\'embed_code_version\' value=\'3\' /> <param name=\'site_root\' value=\'&#47;t&#47;HealthStats\' /><param name=\'name\' value=\'HealthStatsPopulationDashboardbyCountryandGroup-v3_Jun2017&#47;HStatsDashboardbyCountryandGroup\' /><param name=\'tabs\' value=\'no\' /><param name=\'toolbar\' value=\'yes\' /><param name=\'display_count\' value=\'no\' /></object></div>'

@app.route('/search_1')
def search_1():
    return render_template('search_1.html')

@app.route('/search_2')
def search_2():
    return render_template('search_2.html')

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
        state_count[record['state']] = state_count[record['state']] + 1
    json_response = []
    for state,count in state_count.items():
        s_c = {}
        s_c['state'] = state
        s_c['count'] = count
        json_response.append(s_c)
    return jsonify(sorted(json_response, key=lambda x:x['count'], reverse=True)), 200

@app.route("/news", methods=['GET'])
def news():
    RANDOM_TOKEN = 5
    args = get_post_args(['year', 'state'], [str, str])
    year = args.get('year')
    state = args.get('state')
    query = {'date': {'$regex': year}, 'state': state}
    db_cm = mng_db['detailed_gunshot']
    r = db_cm.find(query, {"date":1, 'state':1, 'source_url':1})
    result = []
    for doc in r:
        doc['_id'] = str(doc['_id'])
        result.append(doc)

    url='http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/'
    para = 'urlParagraph'
    title = 'urlTitle'
    content = 'urlParagraph'
    slice = random.sample(result, RANDOM_TOKEN)
    response = []
    for line in slice:
        r_d = {}
        source_url = line['source_url']
        news_title = requests.post(url+title, data={'url': source_url}).text
        rr = re.findall(r"(?=>).*(?=</span>&nbsp)", news_title)
        t = rr[0][1:]
        r_d['title'] = t
        news_content = requests.post(url+content, data={'url': source_url}).text
        rm = re.findall(r"<span class=\"desc\">(.*)(?=</span>)",news_content)
        main = []
        for i in range(1, len(rm)):
            main.append(rm[i])
        r_d['content'] = main
        response.append(r_d)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5500)

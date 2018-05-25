from collections import defaultdict
from flask import Flask, request, render_template, redirect, url_for, make_response, jsonify
from flask_restful import reqparse
import datetime
import json
import requests
import time
import numpy as np
import csv
import pandas as pd
import pymongo
import pprint
from bson import ObjectId
from bson.json_util import loads, dumps

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def convert_to_json():
    source_dict = defaultdict()
    with open('gun_violence_2013_to_2018.csv', 'r', encoding='utf-8-sig', newline='') as raw_data:
        reader = csv.reader(raw_data)
        for row in reader:
            if row[0].startswith('incident_id'):
                continue
            else:
                if row[0] == '':
                    continue
                else:
                    if row[2] in source_dict.keys():
                        source_dict[row[2]].append({'incident_id': row[0],
                                                    'date': row[1],
                                                    'n_killed': row[5],
                                                    'n_injured': row[6]})
                    if row[2] not in source_dict.keys():
                        source_dict[row[2]] = []
                        source_dict[row[2]].append({'incident_id': row[0],
                                                    'date': row[1],
                                                    'n_killed': row[5],
                                                    'n_injured': row[6]})
    json_obj = json.dumps(source_dict, sort_keys=True, indent=4, separators=(',', ': '))
    file_object = open('gun_violence_by_state.json', "w")
    file_object.write(json_obj)
    file_object.close()


def short_name():
    name = defaultdict()
    with open('short_name.txt', 'r') as short:
        for line in short.readlines():
            line.strip()
            name[line[19: -10]] = line[15: 17]
    return name


def grab_from_mlab(short_name):
    source_dict = defaultdict()
    client = pymongo.MongoClient(host='mongodb://LlZzYy:LlZzYy@ds231090.mlab.com:31090/project')
    data_base = client['project']
    data = data_base['detailed_gunshot']
    sn = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona',
         'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
         'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
         'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
         'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
         'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National',
         'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
         'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
         'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina',
         'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
         'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia',
         'WY': 'Wyoming'}
    area = sn[short_name]
    entry_dict = data.find({'state':area})
    for entry in entry_dict:
        if entry['state'] in source_dict.keys():
            source_dict[entry['state']].append({'abbr.': short_name,
                                                '_id': eval(JSONEncoder().encode(entry['_id'])),
                                                'incident_id': entry['incident_id'],
                                                'date': entry['date'],
                                                'n_killed': entry['n_killed'],
                                                'n_injured': entry['n_injured']})
        if entry['state'] not in source_dict.keys():
            source_dict[entry['state']] = []
            source_dict[entry['state']].append({'abbr.': short_name,
                                                '_id': eval(JSONEncoder().encode(entry['_id'])),
                                                'incident_id': entry['incident_id'],
                                                'date': entry['date'],
                                                'n_killed': entry['n_killed'],
                                                'n_injured': entry['n_injured']})

    # json_obj = json.dumps(source_dict, sort_keys=True, indent=4, separators=(',', ': '))
    # pprint.pprint(source_dict)
    return source_dict


def time_cmp(timefrom, timeto, current):
    first_time = datetime.datetime.strptime(timefrom, "%Y-%m-%d").date()
    second_time = datetime.datetime.strptime(timeto, "%Y-%m-%d").date()
    current_time = datetime.datetime.strptime(current, "%Y-%m-%d").date()
    if current_time < first_time or current_time > second_time:
        return False
    if first_time <= current_time <= second_time:
        return True


def query_by_period(short_name, timefrom, timeto):
    short = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona',
             'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
             'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
             'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
             'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
             'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National',
             'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
             'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
             'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina',
             'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
             'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia',
             'WY': 'Wyoming'}
    area = short[short_name]
    # with open('by_state(v1.5).json', 'r') as meta_data:
    outcome = defaultdict()
    outcome[area] = []
    load_dict = grab_from_mlab(short_name)
    for entry in load_dict[area]:
        if not time_cmp(timefrom, timeto, entry['date']):
            continue
        if time_cmp(timefrom, timeto, entry['date']):
            outcome[area].append(entry)
    # json_obj = json.dumps(outcome, sort_keys=True, indent=4, separators=(',', ': '))
    return outcome


def query_by_no_case(short_name, timefrom, timeto):
    short = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona',
             'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
             'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
             'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
             'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
             'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National',
             'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
             'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
             'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina',
             'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
             'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia',
             'WY': 'Wyoming'}
    area = short[short_name]
    # with open('by_state(v1.5).json', 'r') as meta_data:
    outcome = defaultdict()
    output = []
    load_dict = grab_from_mlab(short_name)
    for entry in load_dict[area]:
        if not time_cmp(timefrom, timeto, entry['date']):
            continue
        if time_cmp(timefrom, timeto, entry['date']):
            if entry['date'] not in outcome.keys():
                outcome[entry['date']] = 1
            if entry['date'] in outcome.keys():
                outcome[entry['date']] += 1
    for item in outcome.items():
        output.append({'Date': item[0],
                       'Count': item[1]})
    # json_obj = json.dumps(output, sort_keys=True, indent=4, separators=(',', ': '))
    return output


def victims_count(short_name):
    short = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona',
             'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
             'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
             'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
             'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
             'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National',
             'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
             'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
             'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina',
             'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
             'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia',
             'WY': 'Wyoming'}
    area = short[short_name]
    source_dict = defaultdict(list)
    client = pymongo.MongoClient(host='mongodb://LlZzYy:LlZzYy@ds231090.mlab.com:31090/project')
    data_base = client['project']
    data = data_base['detailed_gunshot']
    for entry in data.find({'state':area}):
        source_dict[entry['state']].append({'abbr.': short_name,
                                            '_id': eval(JSONEncoder().encode(entry['_id'])),
                                            'incident_id': entry['incident_id'],
                                            'date': entry['date'],
                                            'n_killed': entry['n_killed'],
                                            'n_injured': entry['n_injured'],
                                            'victims': entry['n_killed'] + entry['n_injured']})
    json_obj = json.dumps(source_dict, sort_keys=True, indent=4, separators=(',', ': '))
    file_object = open('victims_by_{0}.json'.format(area), "w")
    file_object.write(json_obj)
    file_object.close()

# if __name__ == '__main__':
#     #victims_count('AL')
#     # grab_from_mlab('AL')
#     # query_by_period('AL','2013-07-06','2014-01-01')
#     # query_by_no_case('AL','2013-07-06','2014-01-01')
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/line')
def dataset_page():
    # msg = ''
    # with open('/Users/zhangjiahong/Desktop/9321DataMushup/static/data/beers.csv', 'r') as f:
    #     print(f.readlines())
    with open('/Users/zhangjiahong/Desktop/9321DataMushup/static/lineData/data.json') as f:
        json_dict = json.load(f)
        print(json_dict)
    return jsonify(json_dict)

@app.route('/graph')
def year():
    with open('/Users/zhangjiahong/Desktop/9321DataMushup/static/graph.json') as f:
        json_dict = json.load(f)
        print(json_dict)
    return jsonify(json_dict)

@app.route('/population')
def population_page():
    return '<script type=\'text/javascript\' src=\'http://dataviz.worldbank.org/javascripts/api/viz_v1.js\'></script><div class=\'tableauPlaceholder\' style=\'width: 1080px; height: 1067px;\'><object class=\'tableauViz\' width=\'1080\' height=\'1067\' style=\'display:none;\'><param name=\'host_url\' value=\'http%3A%2F%2Fdataviz.worldbank.org%2F\' /> <param name=\'embed_code_version\' value=\'3\' /> <param name=\'site_root\' value=\'&#47;t&#47;HealthStats\' /><param name=\'name\' value=\'HealthStatsPopulationDashboardbyCountryandGroup-v3_Jun2017&#47;HStatsDashboardbyCountryandGroup\' /><param name=\'tabs\' value=\'no\' /><param name=\'toolbar\' value=\'yes\' /><param name=\'display_count\' value=\'no\' /></object></div>'

@app.route('/search_1')
def search_1():
    return render_template('search_1.html')

@app.route('/search_2')
def search_2():
    return render_template('search_2.html')

@app.route('/map')
def map():
    with open('/Users/zhangjiahong/Desktop/9321DataMushup/static/graph.json') as f:
        json_dict = json.load(f)
        print(json_dict)
    return jsonify(json_dict)


# @app.route('/search?year=2015')
# def getQuery():
#     with open

if __name__ == '__main__':
    app.run(port=5500)

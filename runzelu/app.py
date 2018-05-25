from collections import defaultdict
from dicttoxml import dicttoxml
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
from flask import Flask, request, render_template, redirect, url_for, make_response, jsonify
from flask_restful import reqparse
from functools import wraps
from mongoengine import connect, StringField, IntField, FloatField, Document, EmbeddedDocument, ListField, EmbeddedDocumentField
from werkzeug.contrib.atom import AtomFeed, FeedEntry
import datetime
import json
import requests
import time
import xmltodict
from xml.etree.ElementTree import Element
from data_process import *


app = Flask(__name__)


@app.route('/search?area=<area>&timefrom=<timefrom>&timeto=<timeto>', methods=['GET'])
def search_by_period(area, timefrom, timeto):
    if not area:
        return jsonify(Message='Please input the valid state name.'), 400

    elif not timefrom or not timeto:
        return jsonify(Message='Please specify the start time or end time.'), 400

    return jsonify(query_by_period(area, timefrom, timeto)), 200


@app.route('/graph?area=<area>&timefrom=<timefrom>&timeto=<timeto>', methods=['GET'])
def search_by_no_case(area, timefrom, timeto):
    if not area:
        return jsonify(Message='Please input the valid state name.'), 400

    elif not timefrom or not timeto:
        return jsonify(Message='Please specify the start time or end time.'), 400
    return jsonify(query_by_no_case(area, timefrom, timeto)), 200


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(debug=True)
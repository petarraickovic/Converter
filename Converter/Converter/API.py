from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import wget
import os
import json
from datetime import datetime,timedelta, date
from FileDownloading import DownloadClass
from FileProcessing import ExtractData

app = Flask(__name__)
api = Api(app)

@app.errorhandler(400)
def bad_request(e):
    return e, 400

@app.errorhandler(404)
def not_found(e):
    return e, 404

@app.errorhandler(500)
def not_found(e):
    return "There has been a problem, please try again later", 500

@app.route('/converter', methods=['GET'])
def api_filter():
    query_parameters = request.args

    amount = query_parameters.get('amount')
    try:
        float(amount)
    except ValueError:
        return bad_request("Amount must be a number")

    src_currency = query_parameters.get('src_currency')
    dest_currency = query_parameters.get('dest_currency')
    reference_date = query_parameters.get('reference_date')   
    try:
        datetime.strptime(reference_date, '%Y-%m-%d')
    except ValueError:
        return bad_request("reference_time must be in format YYYY-MM-DD")
    
    
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
    destination = "rates.xml"

    DownloadClass().download_file(url,destination)   

    if(ExtractData().process_file(destination,src_currency, dest_currency, reference_date) == None):
        return not_found("There is no data for the " + reference_date + " date")
    else:
        src_rate, dest_rate = ExtractData().process_file(destination,src_currency, dest_currency, reference_date)

        if(src_rate == None):
            return not_found("There is no data for the " + src_currency + " currency code")

        if(dest_rate == None):
            return not_found("There is no data for the " + dest_currency + " currency code")


    result = float(amount) *float(dest_rate)/float(src_rate)
    response = {}
    response["amount"] = round(result,2)
    response["currency"] = dest_currency

    return jsonify(response)


app.run()
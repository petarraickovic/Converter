
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import wget
import os
import xml.etree.ElementTree as ET
import json
from datetime import datetime,timedelta, date

app = Flask(__name__)
api = Api(app)





class FileProcessing():

    def extract_rates(self,currency, filePart):
        if(currency != 'EUR'):
            try:
                data = next(curr for curr in filePart if(curr.attrib.get('currency') == currency))
            except StopIteration:
                return None
            rate = data.attrib.get('rate')
        else:
            rate = 1
        return rate


    def process_file(self,fileName,src_currency, dest_currency, reference_date):
        tree = ET.parse(fileName)
        root = tree.getroot()
        desiredFilePart = next(child for child in root if('Cube' in child.tag))
        try:
            desiredTime = next(child1 for child1 in desiredFilePart if(child1.attrib.get('time') == reference_date))
        except StopIteration:
            return None
        src_rate = FileProcessing().extract_rates(src_currency, desiredTime)
        dest_rate = FileProcessing().extract_rates(dest_currency, desiredTime)
        return src_rate, dest_rate



class FileDownloading():

    def download_file(self, url, destination):
        if os.path.exists(destination):
            mtime = date.fromtimestamp(os.path.getmtime(destination))
            cur_time = date.today() - timedelta(days = 1)
            if(mtime < cur_time ):
                os.remove(destination)
                wget.download(url, destination)
        else:    
            wget.download(url, destination)
    


@app.errorhandler(400)
def bad_request(e):
    return e, 400

@app.errorhandler(404)
def not_found(e):
    return e, 404

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
    destination = "Rates/rates.xml"

    FileDownloading().download_file(url,destination)   

    if(FileProcessing().process_file(destination,src_currency, dest_currency, reference_date) == None):
        return not_found("There is no data for the " + reference_date + " date")
    else:
        src_rate, dest_rate = FileProcessing().process_file(destination,src_currency, dest_currency, reference_date)

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
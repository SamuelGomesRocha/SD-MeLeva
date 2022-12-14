from flask import Flask, request as req, redirect, url_for, Response as resp
import json
import sys
import xml
from xml.etree.ElementTree import Element as e
sys.path.insert(0, '../')
from service import HoteisService as hs
from flask_cors import CORS
from suds.client import Client
from suds.sudsobject import asdict
from zeep import Client as cz


app = Flask(__name__)

CORS(app)

@app.route('/hoteis/xml', methods = ['GET'])
def getXMLOfHoteis():
    return hs.obtemHoteisXML(1, "2022-02-09", "2022-06-06")


@app.route('/hoteis/json', methods = ['POST'])
def getJSONOfHoteis():
    return hs.obtemHoteisJSON(req.json['id'], req.json['data-inicial'], req.json['data-final'])



if __name__ == "__main__":
    app.run(debug=True)
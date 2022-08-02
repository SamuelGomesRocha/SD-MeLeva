from flask import Flask, request, redirect, url_for, Response as resp
import json
import sys
import xml
from xml.etree.ElementTree import Element as e
sys.path.insert(0, '../')
from flask_cors import CORS
from suds.client import Client
from suds.sudsobject import asdict
from zeep import Client as cz

app = Flask(__name__)

CORS(app)

def initAndReturnHoteis():
    client = Client("http://localhost:8088/mockParceiroAcomodacaoSOAP?wsdl")
    hoteis = client.service.Buscar(1, "2022-02-09", "2022-06-06")
    #wsdl = 'file:///C:/Users/samuh/Documents/SistemasDistribuídos/ContratoParceiro/ParceiroAcomodacao.wsdl'
    #hoteis = cz(wsdl=wsdl).service.Buscar(1, "2022-02-09", "2022-06-06")
    return hoteis

@app.route('/hoteis/xml', methods = ['GET'])
def getXMLOfHoteis():
    response = "\n<hotels>"
    for h in initAndReturnHoteis():
        print(h)
        response += "\n<hotel>"
        response += "\n<name>"+asdict(h).get("nome")+"<name>"
        response += "\n<address>" + asdict(asdict(h).get("endComercial")).get("logradouro") +", "+ str(asdict(asdict(h).get("endComercial")).get("numero"))+ "<address>"
        response += "\n<hotel>"
    response +="\n<hotels>"
    print(response)
    return resp(response, mimetype='text/xml; charset=utf-8')


@app.route('/hoteis/json', methods = ['GET'])
def getJSONOfHoteis():
    response = []
    for h in initAndReturnHoteis():
        response += response + [
            {
                'nome':asdict(h).get("nome"),
                'endereco': {
                    'logradouro': asdict(asdict(h).get("endComercial")).get("logradouro"),
                    'number': str(asdict(asdict(h).get("endComercial")).get("numero"))
                }
            }
        ]
    return json.dumps(response, indent=6)


if __name__ == "__main__":
    app.run(debug=True)
from suds.client import Client
from flask import Response as resp
from suds.sudsobject import asdict
import json


def initAndReturnHoteis(id, dtInicial, dtFinal):
    client = Client("http://localhost:8088/mockParceiroAcomodacaoSOAP?wsdl")
    hoteis = client.service.Buscar(id, dtInicial, dtFinal)
    #wsdl = 'file:///C:/Users/samuh/Documents/SistemasDistribuídos/ContratoParceiro/ParceiroAcomodacao.wsdl'
    #hoteis = cz(wsdl=wsdl).service.Buscar(1, "2022-02-09", "2022-06-06")
    return hoteis

def obtemHoteisJSON(id, dtInicial, dtFinal):
    response = []
    for h in initAndReturnHoteis(id, dtInicial, dtFinal):
        response += response + [
            {
                'nome': asdict(h).get("nome"),
                'endereco': {
                    'logradouro': asdict(asdict(h).get("endComercial")).get("logradouro"),
                    'number': str(asdict(asdict(h).get("endComercial")).get("numero"))
                }
            }
        ]
    return json.dumps(response, indent=6)

def obtemHoteisXML(id, dtInicial, dtFinal):
    response = "\n<hotels>"
    for h in initAndReturnHoteis(id, dtInicial, dtFinal):
        print(h)
        response += "\n<hotel>"
        response += "\n<name>" + asdict(h).get("nome") + "<name>"
        response += "\n<address>" + asdict(asdict(h).get("endComercial")).get("logradouro") + ", " + str(
            asdict(asdict(h).get("endComercial")).get("numero")) + "<address>"
        response += "\n<hotel>"
    response += "\n<hotels>"
    print(response)
    return resp(response, mimetype='text/xml; charset=utf-8')
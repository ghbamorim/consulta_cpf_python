import sys

sys.path.append(".")
import requests, base64, json
import datetime
from .params import Token_params, Cpf_params

statusCodes = {
    0: "Regular",
    2: "Suspenso",
    3: "Falecido",
    4: "Pendente de Regularização",
    5: "Cancelada",
    8: "Nula",
    9: "Cancelada de Ofício"
}


class Serpro_intf():
    #Token armazenado expira 5 minutos antes
    expiration_window = 6900
    lastTokenTime = 0
    access_token = ""

    def consultaCpf(self, data: Cpf_params):
        compare_date = datetime.datetime.now() - datetime.timedelta(
            seconds=Serpro_intf.expiration_window)

        if (Serpro_intf.lastTokenTime
                == 0) or (Serpro_intf.lastTokenTime < compare_date):
            Serpro_intf.access_token = self.getToken(data)
            Serpro_intf.lastTokenTime = datetime.datetime.now()

        uri = "https://h-apigateway.conectagov.estaleiro.serpro.gov.br/api-cpf-light/v2/consulta/cpf"
        headers = {
            "content-type": "application/json; charset=utf-8",
            "x-cpf-usuario": data.user_cpf,
            "authorization": "Bearer %s" % Serpro_intf.access_token
        }

        json_cpf = {"listaCpf": [data.cpf_for_query]}
        response = requests.post(url=uri, headers=headers, json=json_cpf)
        json_response = json.loads(response.content)

        result = None

        for cpf in json_response:
            result = {"status": statusCodes[cpf["SituacaoCadastral"]]}
        return result, json_response, response.status_code

    def getToken(self, data: Token_params) -> str:
        uri = "https://h-apigateway.conectagov.estaleiro.serpro.gov.br/oauth2/jwt-token"
        authorization_base64 = base64.b64encode(
            str(data.client_id + ":" + data.client_secret).encode("utf-8"))
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Basic %s" % str(authorization_base64, "utf-8")
        }
        params = {
            "grant_type": "client_credentials",
            "scope": "api-cpf-light-v1"
        }
        response = requests.post(url=uri, headers=headers, data=params)

        json_response_token = json.loads(response.content)
        return json_response_token["access_token"]
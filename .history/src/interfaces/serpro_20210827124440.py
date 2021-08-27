import sys
sys.path.append(".")
import requests, base64, json
import datetime

class Token_params:
  client_id : str
  client_secret : str  
  
class Cpf_params(Token_params):
  user_cpf : str
  cpfs_for_query : str


class Serpro_intf():
    #Expira 5 minutos antes
    expiration_window = 6900
    lastTokenTime = datetime.datetime.now()
    access_token = '';      

    def consultaCpf(self, data : Cpf_params):        
        compare_date = datetime.datetime.now() - datetime.timedelta(seconds=Serpro_intf.expiration_window)
        #print("compare_date = " + str(compare_date))
        global access_token
        if (Serpro_intf.lastTokenTime == 0) or (Serpro_intf.lastTokenTime < compare_date):
            access_token = self.getToken(data)
            Serpro_intf.lastTokenTime=datetime.datetime.now()

        #x_cpf_usuario = data.user_cpf #'00993162428'

        uri = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br/api-cpf-light/v2/consulta/cpf'
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'x-cpf-usuario': data.user_cpf,
            'authorization': 'Bearer %s' % access_token
        }

        json_cpf = {
            "listaCpf": [
                data.cpfs_for_query
            ]
        }
        response = requests.post(url = uri, headers = headers, json = json_cpf)
        json_response = json.loads(response.content)
        print(json_response)
        return json_response

    def getToken(self, data : Token_params) -> str:
        uri = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br/oauth2/jwt-token'
        #client_id = '8ddc46f2-f6a3-4077-9e04-74b55de934a5'
        #client_secret = '06d4aaac-1412-45f6-bd7c-38b2bef0d706'
        authorization_base64 = base64.b64encode(str(data.client_id + ':' + data.client_secret).encode('utf-8'))
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'Basic %s' % str(authorization_base64, 'utf-8')
        }
        params = {        'grant_type': 'client_credentials',        'scope': 'api-cpf-light-v1'    }
        response = requests.post(url = uri, headers = headers, data = params)
        json_response_token = json.loads(response.content)
        return json_response_token['access_token']
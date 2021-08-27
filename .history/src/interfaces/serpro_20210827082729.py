import requests, base64, json
import datetime

lastTokenTime = datetime.datetime.now()
access_token = '';
expiration_window_sec = 300

def consultaCpf(cpf):
    global lastTokenTime
    #print(datetime.datetime.now() + datetime.timedelta(seconds=expiration_window_sec)
    compare_date = datetime.datetime.now() + datetime.timedelta(seconds=expiration_window_sec)
    print(compare_date)

    if (lastTokenTime == 0) or (lastTokenTime < compare_date):
        access_token = getToken()
        lastTokenTime=datetime.datetime.now()

    x_cpf_usuario = '00993162428'

    uri = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br/api-cpf-light/v2/consulta/cpf'
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'x-cpf-usuario': x_cpf_usuario,
        'authorization': 'Bearer %s' % access_token
    }

    json_cpf = {
        "listaCpf": [
            cpf
        ]
    }
    response = requests.post(url = uri, headers = headers, json = json_cpf)
    json_response = json.loads(response.content)
    print(json_response)
    return json_response


def getToken():
    uri = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br/oauth2/jwt-token'
    client_id = '8ddc46f2-f6a3-4077-9e04-74b55de934a5'
    client_secret = '06d4aaac-1412-45f6-bd7c-38b2bef0d706'
    authorization_base64 = base64.b64encode(str(client_id + ':' + client_secret).encode('utf-8'))
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'authorization': 'Basic %s' % str(authorization_base64, 'utf-8')
    }
    params = {        'grant_type': 'client_credentials',        'scope': 'api-cpf-light-v1'    }
    response = requests.post(url = uri, headers = headers, data = params)
    json_response_token = json.loads(response.content)
    return json_response_token['access_token']

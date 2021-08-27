# configurações iniciais
import requests, base64, json
# recuperando token de acesso
try:
    uri = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br/oauth2/jwt-token'    
    client_id = '8ddc46f2-f6a3-4077-9e04-74b55de934a5'
    client_secret = '06d4aaac-1412-45f6-bd7c-38b2bef0d706'
    x_cpf_usuario = '00993162428'
    authorization_base64 = base64.b64encode(str(client_id + ':' + client_secret).encode('utf-8'))
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'authorization': 'Basic %s' % str(authorization_base64, 'utf-8')
    }
    params = {        'grant_type': 'client_credentials',        'scope': 'api-cpf-light-v1'    }
    response = requests.post(url = uri, headers = headers, data = params)
    json_response_token = json.loads(response.content)
    access_token = json_response_token['access_token']
except Exception as exc:
  print('Erro ao recuperar token:', exc)

# requisição API
try:
    uri = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br/api-cpf-light/v2/consulta/cpf'
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'x-cpf-usuario': x_cpf_usuario,
        'authorization': 'Bearer %s' % access_token
    }

     # lista de CPFs a serem consultados
    json_cpf = {
       "listaCpf": [
           "77689062768",
           "00045024936",
           "01182101062",
           "21316016897",
           "26616776824",
           "72002557853",
           "90678117934",
           "82272182100",
           "82272387187",
           "82271577187"
       ]
    }
    response = requests.post(url = uri, headers = headers, json = json_cpf)
    json_response = json.loads(response.content)
except Exception as exc:    
    print('Erro ao recuperar informações:', exc)
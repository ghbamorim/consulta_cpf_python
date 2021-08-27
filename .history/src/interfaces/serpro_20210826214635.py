import requests
response = requests.get('https://api.buildkite.com/v2/organizations/orgName/pipelines/pipelineName/builds/1230', headers={ 'Authorization': 'Bearer <your_token>' })
print response.json()
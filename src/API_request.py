import json
import requests
from config import config

payload = {}

token = config["token"]
url = config["url"]


def getProjectPipelines(base_url, organization, project):
    url = f'{base_url}/{organization}/{project}/_apis/pipelines?api-version=6.0-preview.1'
    headers = {'Authorization': f'Basic {token}'}
    return requests.request("GET", url, headers=headers, data=payload).json().get('value')


def findPipelineByName(pipelines, name):
    for pipeline in pipelines:
        if pipeline.get('name') == name:
            return pipeline
    return None


def runPipeLine(base_url, organization, project, pipelineId):
    payload = json.dumps({
        "resources": {
            "repositories": {
                "self": {
                    "refName": "refs/heads/main"
                }
            }
        }
    })
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Basic {token}'}
    url = f'{base_url}/{organization}/{project}/_apis/pipelines/{pipelineId}/runs?api-version=6.0-preview.1'
    return requests.request("POST", url, headers=headers, data=payload)

def API_request(projectOrganization,projectName):
    pipelines = getProjectPipelines(url, projectOrganization, projectName)
    pipeline = findPipelineByName(pipelines, 'CI')
    return runPipeLine(url, projectOrganization, projectName, pipeline.get('id')).status_code == 200
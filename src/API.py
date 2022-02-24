import json
from typing import Dict, List

import requests

from config import config
from log import config_logger

logger = config_logger()
payload = {}

token = config["token"]
url = config["url"]


def get_project_pipelines(base_url: str, organization: str, project: str) -> List[Dict[str, str]]:
    url = f'{base_url}/{organization}/{project}/_apis/pipelines?api-version=6.0-preview.1'
    headers = {'Authorization': f'Basic {token}'}
    return requests.request("GET", url, headers=headers, data=payload).json().get('value')


def find_pipeline_by_name(pipelines: List[Dict[str, str]], name: str):
    for pipeline in pipelines:
        if pipeline.get('name') == name:
            return pipeline
    return None


def send_azure_run_requset(base_url: str, organization: str, project: str, pipelineId: str) -> requests.Response:
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


def run_ci_pipline(projectOrganization: str, projectName: str) -> None:
    logger.info('start API request process')
    pipelines = get_project_pipelines(url, projectOrganization, projectName)
    pipeline = find_pipeline_by_name(pipelines, 'CI')
    if send_azure_run_requset(url, projectOrganization, projectName, pipeline.get('id')).status_code == 200:
        logger.info('CI pipeline run successfully')
        logger.info('API request process finished')
    else:
        logger.critical('CI pipeline run failed')

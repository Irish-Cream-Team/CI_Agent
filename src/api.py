import json
from typing import Dict, List

import requests

from config import Config
from custom_error import *
from log import Logger


class API:

    def __init__(self, organization: str, project: str, config: Config, logger: Logger):
        """
        Initializes the API class.
        :param organization: Azure organization name.
        :param project: Azure project name.
        """
        self.config = config
        self.logger = logger
        self.organization = organization
        self.project = project
        self.api_version = '?api-version=6.0-preview.1'

    def get_project_pipelines(self) -> List[Dict[str, str]]:
        """
        Get the project pipelines. 
        :return: List of pipelines.
        """
        url = f'{self.get_project_pipelines_url}{self.get_api_version()}'
        headers = {'Authorization': f'Basic {self.config.get_token()}'}

        return requests.request("GET", url, headers=headers, data={}).json().get('value')

    def find_pipeline_by_name(self, name: str) -> Dict[str, str]:
        """
        Finds a pipeline by name.
        :param name: Pipeline name.
        :return: Pipeline details.
        """
        pipelines = self.get_project_pipelines()
        for pipeline in pipelines:
            if pipeline.get('name') == name:
                return pipeline

        raise PipelineNotFoundError(f'Pipeline with name {name} not found')

    def get_pipeline_id_by_name(self, name: str) -> str:
        """
        Find a pipeline by name.
        :param name: Pipeline name.
        :return: Pipeline ID.
        """
        pipeline = self.find_pipeline_by_name(name)
        return pipeline.get('id') or ''

    @staticmethod
    def create_payload() -> str:
        """
        Creates the payload for the pipeline run request.
        :return: Payload.
        """

        payload = json.dumps({
            "resources": {
                "repositories": {
                    "self": {
                        "refName": "refs/heads/main"
                    }
                }
            }
        })
        return payload

    def create_headers(self) -> Dict[str, str]:
        """
        Creates the headers for the pipeline run request with authorization.
        :return: Headers.
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.config.get_token()}'
        }
        return headers

    def get_organization(self) -> str:
        """
        Get the organization.
        :return: Organization.
        """

        return self.organization

    def get_project(self) -> str:
        """
        Get the project.
        :return: Project.
        """

        return self.project

    def get_project_pipelines_url(self) -> str:
        """
        Get the project API pipelines URL.
        :return API pipelines URL.
        """

        return f'{self.config.get_azure_url()}/{self.organization}/{self.project}/_apis/pipelines'

    def get_api_version(self) -> str:
        """
        Get the API version.
        :return API version.
        """

        return self.api_version

    def get_project_pipeline_runs_url(self, pipeline_id: str) -> str:
        """
        Get the project API pipeline runs URL.
        :return API pipeline runs URL.
        """

        return f'{self.get_project_pipelines_url()}/{pipeline_id}/runs{self.get_api_version()}'

    def send_pipeline_run(self, pipeline_id: str) -> requests.Response:
        """
        Send a pipeline run request.
        :param pipeline_id: Pipeline ID.
        :return: Azure run request Response.
        """

        url = self.get_project_pipeline_runs_url(pipeline_id)
        headers = self.create_headers()
        payload = self.create_payload()

        return requests.request("POST", url, headers=headers, data=payload).json()

    def run_ci_pipline(self) -> None:
        """
        Runs the CI pipeline.
        """
        self.logger.info('start API request process')
        pipeline_id = self.get_pipeline_id_by_name('CI')

        if self.send_pipeline_run(pipeline_id).status_code == 200:
            self.logger.info('CI pipeline run successfully')
            self.logger.info('API request process finished')
        else:
            raise APIError('API request failed')

    @staticmethod
    def check_url(url: str) -> bool:
        """
        Check if the URL is valid.
        :param url: URL.
        :return: True if valid, False if not.
        """
        status_code = requests.head(url).status_code
        return status_code == 200

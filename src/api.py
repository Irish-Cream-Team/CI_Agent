import json
from typing import Dict, List

import requests

from config import *
from custom_error import *
from logger import Logger


class API:

    def __init__(self, organization: str, project: str, config: Dict[str, str], logger: Logger):
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
        self.azure_url = Config.get_azure_url(self.config)
        self.azure_token = Config.get_token(self.config)

    def __get_project_pipelines(self) -> List[Dict[str, str]]:
        """
        Get the project pipelines. 
        :return: List of pipelines.
        """
        url = f'{self.__get_project_pipelines_url()}{self._get_api_version()}'
        headers = {'Authorization': f'Basic {self.azure_token}'}
        return requests.request("GET", url, headers=headers, data={}).json().get('value')

    def _find_pipeline_by_name(self, name: str) -> Dict[str, str]:
        """
        Finds a pipeline by name.
        :param name: Pipeline name.
        :return: Pipeline details.
        """
        pipelines = self.__get_project_pipelines()
        for pipeline in pipelines:
            if pipeline.get('name') == name:
                return pipeline

        raise PipelineNotFoundError(f'Pipeline with name {name} not found')

    def _get_pipeline_id_by_name(self, name: str) -> str:
        """
        Find a pipeline by name.
        :param name: Pipeline name.
        :return: Pipeline ID.
        """
        pipeline = self._find_pipeline_by_name(name)
        return pipeline.get('id') or ''

    @staticmethod
    def _create_payload() -> str:
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

    def _create_headers(self) -> Dict[str, str]:
        """
        Creates the headers for the pipeline run request with authorization.
        :return: Headers.
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.azure_token}'
        }
        return headers

    def _get_organization(self) -> str:
        """
        Get the organization.
        :return: Organization.
        """

        return self.organization

    def _get_project(self) -> str:
        """
        Get the project.
        :return: Project.
        """

        return self.project

    def __get_project_pipelines_url(self) -> str:
        """
        Get the project API pipelines URL.
        :return API pipelines URL.
        """

        return f'{self.azure_url}/{self.organization}/{self.project}/_apis/pipelines'

    def _get_api_version(self) -> str:
        """
        Get the API version.
        :return API version.
        """

        return self.api_version

    def __get_project_pipeline_runs_url(self, pipeline_id: str) -> str:
        """
        Get the project API pipeline runs URL.
        :return API pipeline runs URL.
        """

        return f'{self.__get_project_pipelines_url()}/{pipeline_id}/runs{self._get_api_version()}'

    def _send_pipeline_run(self, pipeline_id: str) -> requests.Response:
        """
        Send a pipeline run request.
        :param pipeline_id: Pipeline ID.
        :return: Azure run request Response.
        """

        url = self.__get_project_pipeline_runs_url(pipeline_id)
        headers = self._create_headers()
        payload = self._create_payload()
        return requests.request("POST", url, headers=headers, data=payload)

    def run_ci_pipline(self) -> None:
        """
        Runs the CI pipeline.
        """
        self.logger.info('start API request process')
        pipeline_id = self._get_pipeline_id_by_name('CI')

        if self._send_pipeline_run(pipeline_id).status_code == 200:
            self.logger.info('CI pipeline run successfully')
            self.logger.info('API request process finished')
        else:
            raise APIError('API request failed')

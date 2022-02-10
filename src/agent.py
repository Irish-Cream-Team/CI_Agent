import os
import shutil
import json

from API_request import API_request

def on_create(event):

    main(event.src_path)


def main(filePath):
    info  = os.getxattr(filePath, 'user.info').decode("utf-8")
    info = json.loads(info)
    path = info.get('path')
    projectName = info.get('projectName')
    projectOrganization = info.get('projectOrganization')
    shutil.move(filePath, path)
    print(f'File moved to {path}')
    API_request(projectOrganization, projectName)


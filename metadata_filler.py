import os
import json
TeamName = 'TeamName'
AzureProjectName = 'Halbana'
AzureProjectOrganization = 'yesodot'

filePath = '/home/ofek/Documents/CI_Agent/test/bigGoodFile.txt'
info = {'TeamName': TeamName,
        'AzureProjectName': AzureProjectName,
        'AzureProjectOrganization': AzureProjectOrganization}


def dict_to_binary(dict):
    str = json.dumps(dict)
    return str.encode('utf-8')


os.setxattr(filePath, 'user.info', dict_to_binary(info))

info = os.getxattr(filePath, 'user.info').decode("utf-8")

print(info)

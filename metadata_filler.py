import os
import json
path = '/home/ofek/Documents/aramy/Inside_CI/Yesodot/TeamName/ProjectName/Images'
projectName = 'Halbana'
projectOrganization = 'yesodot'
filePath = 'foo.txt'
info = {'path': path, 'projectName': projectName,
        'projectOrganization': projectOrganization}


def dict_to_binary(dict):
    str = json.dumps(dict)
    return str.encode('utf-8')




os.setxattr('foo.txt', 'user.info', dict_to_binary(info))

info = os.getxattr(filePath, 'user.info').decode("utf-8")

print(info)

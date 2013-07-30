'''
Created on 29.07.2013

@author: mhoyer
'''

class Application():
    '''
    classdocs
    '''


    def __init__(self, app_dict):
        self.url = app_dict["url"]
        self.files = app_dict["files"]
        self.folders = app_dict["folders"]
        self.databases = app_dict["databases"]
        self.packages = app_dict["packages"]
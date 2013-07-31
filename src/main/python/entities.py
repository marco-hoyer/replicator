'''
Created on 29.07.2013

@author: mhoyer
'''

class Application():

    def __init__(self, app_dict):
        self.name = app_dict["name"]
        self.url = app_dict["url"]
        self.files = app_dict["files"]
        self.master_node = app_dict["master_node"]
        self.slave_node = app_dict["slave_node"]
        self.folders = app_dict["folders"]
        self.databases = app_dict["databases"]
        self.packages = app_dict["packages"]
        self.needed_services = app_dict["needed_services"]
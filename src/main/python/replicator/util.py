import os
import datetime

'''
Created on 07.10.2013

@author: mhoyer
'''

# TODO: check items for spaces and special chars
# TODO: remove double slashes
def path_append(path_items):
    path = ""
    for item in path_items:
        if not item.startswith("/") and not item.startswith("."):
            path = path + "/"
        path = path + item
    path = os.path.normpath(path)
    return path

def get_timestamp():
    date = datetime.datetime.now()
    return date.strftime("%d-%m-%Y_%H-%M")
        
def get_folder_from_path(path):
    return os.path.split(path)[0]
    
def get_filename_from_path(path):
    return os.path.split(path)[1]
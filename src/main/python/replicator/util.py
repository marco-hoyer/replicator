import os

'''
Created on 07.10.2013

@author: parallels
'''

# TODO: check items for spaces and special chars
# TODO: remove double slashes
def path_append(path_items):
    path = ""
    for item in path_items:
        if not item.startswith("/"):
            path = path + "/"
        path = path + item
    path = os.path.normpath(path)
    return path
        
def get_folder_from_path(path):
    return os.path.split(path)[0]
    
def get_filename_from_path(path):
    return os.path.split(path)[1]
import os
from pathlib import Path
import json
import filetype

# Find desktop location
def get_desktop_location():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    return desktop

# Find Downloads location
def get_downloads_location():
    downloads = Path.home() / 'Downloads'
    return str(downloads)

def is_filename_valid(filename):
    acceptable_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ^&'@[],$=!-#()%.+~_"
    for character in filename:
        if character not in acceptable_characters:
            return False
    return True

# Checks if a filename has a specified file extension
def has_proper_extension(filename, ext):
    return True if filename[-4:] == ext else False

# Adds an extension to a filename
def add_extension(filename, ext):
     return filename + ext

# Adds Desktop path to filename
def add_desktop_path_to_filename(filename):
    return f'{get_desktop_location()}\{filename}'

# Create a folder on the desktop
def create_folder_on_desktop(folder):
    try:
        save = get_desktop_location()
        os.mkdir(save + '/' + folder)     
        return True
    except:
        return False

# Create a folder in downloads
def create_folder_in_downloads(folder):
    try:
        save = get_downloads_location()
        os.mkdir(save + '/' + folder)     
        return True
    except:
        return False

# Check if a JSON file is Valid
def JSON_is_valid(json_file):
    try:
        json.load(open(json_file))
    except:
        return False
    return True

# Check if a file exists
def file_exists(file_path):
    return True if os.path.isfile(file_path) else False

# Check if files in a list exists
def check_files(list):
    list_of_invalid_files = []
    for file in list:
        if file_exists(file) == False:
            list_of_invalid_files.append(file)
    return list_of_invalid_files

# Check if a folder exists
def folder_exists(folder_path):
    return True if os.path.isdir(folder_path) else False


def is_correct_file_type(file, expected_file_type):
    formats = {'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' : 'Excel',
               'application/pdf' : 'PDF'}

    kind = filetype.guess(file)

    if kind is None:
        return False
    
    return True if kind.mime in formats and  expected_file_type == formats[kind.mime] else False
    
    
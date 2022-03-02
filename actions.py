import os
import sys
import json
import urllib.request
from pathvalidate import sanitize_filename


URL = 'https://raw.githubusercontent.com/Diogo-Rossi/ConfigFiles/public/actions-diogo.json'

class Actions:
    
    def __init__(self, path=''):
        config_link = URL
        self.path = path
        self.config = self.__loadConfig(config_link)
        self.actions = self.__loadActions(self.config)
    
    def __loadConfig(self, link):
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
        return data
    
    def __loadActions(self, config):
        return [item['type'] for item in config]
    
    def __createFoldersFromList(self, folders, baseFolder=''):
        baseFolder = sanitize_filename(baseFolder)
    
        for folder in folders:
            if input("> Create folder '" + folder + "' ([y]/n)? ") != "n":
                folderName = os.path.join(self.path, baseFolder, folder)
                os.makedirs(folderName, True)
    
    def __downloadFilesFromList(self, files, baseFolder=''):
        baseFolder = sanitize_filename(baseFolder)
        for file in files:
            link = file["from"]
            destination = file["to"]
            fileName = link.rsplit("/", 1)[-1]
            if input("\n> Create file '" + fileName + "' ([y]/n)? ") != "n":
                fullPathFile = os.path.join(
                    self.path, baseFolder, destination, fileName)
                
                if not os.path.isfile(fullPathFile):
                    print(f'DOWNLOADING.... {link}')
                    urllib.request.urlretrieve(link, fullPathFile)
    
    def doActions(self, actionType, folderName):
        [actions] = [item['actions']
                     for item in self.config if (item['type'] == actionType)]
        
        self.__createFoldersFromList(actions['folders'], folderName)
        self.__downloadFilesFromList(actions['files'], folderName)


def initApp(myActions):
    # INTERFACE VIA TERMINAL
    print("============================================")
    print(" CHOOSE ONE OPTION: ")
    print("============================================")
    optionNumber = 0
    for action in myActions.actions:
        optionNumber += 1
        print(f" {optionNumber} - {action}")
    optionSelected = int((lambda x: -1 if x == '' else x)(input("> ")))
    if optionSelected < 0: sys.exit()
    
    print("============================================")
    print(" FOLDER NAME: ")
    print("============================================")
    folderName = input("> ")
    
    print("============================================")
    print(" CONFIRM ([y]/n)? ")
    print(f": {myActions.actions[optionSelected-1]}")
    print(f": {folderName}")
    print("============================================")
    confirm = (input("> "))
    # ./INTERFACE VIA TERMINAL
    
    if confirm != "n":
        myActions.doActions(myActions.actions[optionSelected-1], folderName)
    
    input("\n: Press ENTER to finish... ")


path = '.' if sys.argv else sys.argv[1]
action = Actions(path)
initApp(action)

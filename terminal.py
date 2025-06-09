class folder():
    def __init__(self, name, content = []):
        self.name = name
        self.content = content
        pass

class file():
    def __init__(self, name):
        sufix = "none"
        self.content = ""
        self.name = ""
        self.setFullName(name, sufix)
        pass

    def setFullName(self, name, sufix):
        self.name = name + "." + sufix

class txtClass(file):
    def __init__(self, name, content = ""):
        super().__init__(name)
        sufix = "txt"
        self.sufix = sufix
        self.setFullName(name, sufix)
        self.content = content

class pythonClass(file):
    def __init__(self, name, content = ""):
        super().__init__(name)
        sufix = "py"
        self.sufix = sufix
        self.setFullName(name, sufix)
        self.content = content

filesStructure = folder(name="folderStructure", content=[
    folder(name="~", content=[
        folder("Applications", []),
        folder("System", []),
        folder("Users", [
            folder("James", [
                txtClass("tt", content="hello, this is just a test.\nIn case you found this file it means that you are capable of using the basics of as terminal :)")
            ])
            ])
    ])
])

sufixesDict = {
    "txt" : txtClass,
    "py" : pythonClass
    }

writableFiles = ["py", "txt"]

currentFolderPath = "~"

def checkForItemName(itemName, itemClass,lst : list):
    
    for item in lst:
        if isinstance(item, itemClass) == False:
            continue
        if item.name == itemName:
            return item
    if isinstance(item, folder):
        return "no folder found with that name"
    elif isinstance(item, file):
        return "no file found with that name"

def searchByPath(path : str, finalFileType : str):
    """
    Files type:
    'folder' -> folder class
    'file' -> file class
    """
    global filesStructure

    searchClass = None
    if finalFileType == "folder":
        searchClass = folder
    elif finalFileType == "file":
        searchClass = file
    else:
        return "Please Input a valid sufix"

    pathItems = path.split("/")
    currentFolder = filesStructure
    for i in range(len(pathItems)):
        if i+1 >= len(pathItems):
            rsp = checkForItemName(pathItems[i], searchClass, currentFolder.content)
            if isinstance(rsp, searchClass):
                currentFolder = rsp
                break
            print("hey, Programmer, PLEASE MAJKE SURE YOU ARE USING THE CORRECT finalFileType ----------------")
            return False    

        rsp = checkForItemName(pathItems[i], folder, currentFolder.content)
        if isinstance(rsp, folder):
            currentFolder = rsp
            continue
        print("hey, Programmer, PLEASE MAJKE SURE YOU ARE USING THE CORRECT finalFileType ----------------")
        return False
    return currentFolder


def getFileNames(lstFolder : list):
    names = []
    for item in lstFolder:
        names.append(item.name)
    return names

def checkIfFileNameExists(fileName):
    currentFolder = searchByPath(currentFolderPath, "folder")
    folderNames = getFileNames(currentFolder.content)
    if fileName not in folderNames:
        return True
    return False

def addFileToFolder(folderPath, fileClass):
    folder = searchByPath(folderPath, "folder")
    if checkIfFileNameExists(fileClass.name):
        folder.content.append(fileClass)
        return
    return "folder name cannot exist already"
# files = ["User", "Desktop", "Downloads"]

def ls(inputList):
    global currentFolderPath
    currentFolder = searchByPath(currentFolderPath, "folder")
    if currentFolder:
        folderItems = currentFolder.content
    else:
        return "The folder wasnt found? kkkkk"
    if(len(folderItems) > 0):
        
        names = getFileNames(folderItems)
        # print(names)
        return " | ".join(names)
    return " "

def cd(inputList):
    global currentFolderPath
    
    if len(inputList) < 2:
        currentFolderPath = "~"
        return
    path = inputList[1]
    # print(path)
    if path == "~" or path == "..":
        currentFolderPath = "~"
        return
    folderPath = currentFolderPath + "/" + path
    if searchByPath(folderPath,"folder"):
        currentFolderPath = folderPath
    else:
        return "there is no such file or directory"

def mkdir(inputList):
    global currentFolderPath
    if len(inputList) < 2:
        return "you gotta give a name to the folder you are creating"
    folderName = inputList[1]
    answer = addFileToFolder(currentFolderPath, folder(folderName, []))
    return answer

def pwd(inputList):
    global currentFolderPath
    return currentFolderPath

def cat(inputList):
    global currentFolderPath
    if len(inputList) < 2:
        return "you gotta give a name to the file you wanna read"
    fullFileName = inputList[1]
    if ("." in fullFileName) == False:
        return "please add the sufix of the file you want to read.\nExample: 'TextFile.txt'"
    fileName = fullFileName.split(".")[0]
    fileSufix = fullFileName.split(".")[1]
    if fileSufix not in sufixesDict.keys():
        return "please enter a valid sufix"
    fullPath = f"{currentFolderPath}/{fullFileName}"
    fileRead = searchByPath(fullPath, "file")
    if fileRead:
        return fileRead.content
    return "there is no such file or directory"

def touch(inputList):
    global currentFolderPath
    if len(inputList) < 2:
        return "you gotta give a name to the file you wanna read"
    fullFileName = inputList[1]
    if ("." in fullFileName) == False:
        return "please add the sufix of the file you want to read.\nExample: 'TextFile.txt'"
    fileName = fullFileName.split(".")[0]
    fileSufix = fullFileName.split(".")[1]
    if fileSufix not in sufixesDict.keys():
        return "please enter a valid sufix"
    fileClass = sufixesDict[fileSufix](fileName)
    ansewr = addFileToFolder(currentFolderPath, fileClass)
    return ansewr
    
def echo(inputList):
    global currentFolderPath, writableFiles
    if len(inputList) < 4:
        return "please use help echo to see how to utilize it correctly"
    
    fullFileName = inputList[-1]
    if ("." in fullFileName) == False:
        return "please add the sufix of the file you want to read.\nExample: 'TextFile.txt'"
    fileName = fullFileName.split(".")[0]
    fileSufix = fullFileName.split(".")[1]
    if fileSufix not in writableFiles:
        return "please enter a valid sufix"
    pathToFile = currentFolderPath + "/" + fullFileName
    file = searchByPath(pathToFile, "file")
    if not file:
        print(pathToFile)
        return "please add a valid file"
    
    textList = inputList[1:-2]
    if '"' in textList[0]:
        textList[0] = textList[0].replace('"', '')
    if '"' in textList[-1]:
        textList[-1] = textList[-1].replace('"', '') 
    text = " ".join(textList)
    arr = inputList [-2]
    if arr == ">":
        file.content = text
    elif arr == ">>":
        file.content += f"\n{text}"
    else:
        return "please use help echo to see how to utilize it correctly"
    
def python(inputList):
    global currentFolderPath, writableFiles
    if len(inputList) < 2:
        return "you gotta give a name to the file you wanna read"

    fullFileName = inputList[1]
    if ("." in fullFileName) == False:
        return "please add the sufix of the file you want to read.\nExample: 'TextFile.txt'"
    
    fileName = fullFileName.split(".")[0]
    fileSufix = fullFileName.split(".")[1]
    if fileSufix not in writableFiles:
        return "please enter a valid sufix"
    
    pathToFile = currentFolderPath + "/" + fullFileName

    file = searchByPath(pathToFile, "file")
    if not file:
        print(pathToFile)
        return "please add a valid file"
    
    fileContent = file.content
    try:
        exec(fileContent)
    except Exception as e:
        return e



commds = {
    "ls" : ls,
    "cd" : cd,
    "mkdir" : mkdir,
    "pwd" : pwd,
    "cat" : cat,
    "touch" : touch,
    "echo" : echo,
    "python" : python
}

# def useTerminal(string : str):
    # currentFolderPath = ""

ut = True
while ut:
    currentFolder = currentFolderPath.split("/")[-1]
    inp = input(f"\033[32m{currentFolder} % ")
    print("\033[0m", end="")
    if inp:
        if inp == "quit":
            ut = False
            continue
        
        comandos = commds.keys()

        inputList = inp.split(" ")

        firstCommand = inputList[0]

        if firstCommand not in comandos:
            print(f"Command not recognized")
            continue
        # len(inputList)
        # print(inputList)
        # print()
        response = commds[firstCommand](inputList)
        if response:
            print(response)



        
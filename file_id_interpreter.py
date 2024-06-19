
class FileIdInterpreter:
    """
    Class that when given an ID dictionary file, can interpret the information in that file and return as a list

    Attributes:
        file_name (str): string that represents the file containing the ID dict.
        id (str): ID to look for

    Methods:
        interpretFileInfo(self): interprets file and returns a list with the attributes associated with ID.
    """
    
    # Attributes
    __file_name = None
    __id = None

    # Constructor
    def __init__(self, file_name, id):
        self.setFileName(file_name)
        self.setId(id)

    # Getters
    def getFileName(self):
        return self.__file_name
    def getId(self):
        return self.__id

    # Setters
    def setFileName(self, file_name):
        self.__file_name = file_name
    def setId(self, id):
        self.__id = id

    # Methods
    def interpretFileInfo(self):
        """
        Finds ID in file named file_name, then returns a list containing all info associated with that ID
        """
        with open(self.getFileName(), 'r') as file:
                str_to_find = '!!' + self.getId() # !!{ID} marker
                file_lines = file.readlines()
                for line in file_lines:
                    if str_to_find in line: # if line contains ID, immediately returns list containing that info
                        return [i for i in line.split('~')[1].split('/')] 
        
        # If no object matching ID is found.
        raise Exception(f"No object with ID {self.getId()} found")

class FileIdInterpreter:
    """
    Class containing method interpretFileInfo, which interprets *_id files

    Methods:
        interpretFileInfo(self): interprets file and returns a list with the attributes associated with ID.
    """

    # Methods
    def interpretFileInfo(self, file_name: str, id: str) -> list[str]:
        """
        Finds ID in file named file_name, then returns a list containing all info associated with that ID
        """
        with open(file_name, 'r') as file:
                str_to_find = '!!' + id # string to look for in the id file
                file_lines = file.readlines()
                for line in file_lines:
                    if str_to_find in line: # if line contains ID, immediately returns list containing that info
                        return [i for i in line.split('~')[1].split('/')] 
        
        # If no object matching ID is found.
        raise Exception(f"No object with ID {id} found")
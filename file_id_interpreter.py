
class FileIdInterpreter:
    """Class containing method for interpreting '*_id' files."""

    # Methods
    def interpretFileInfo(self, file_name: str, id: str) -> list[str]:
        """
        Finds ID in file named file_name, then returns a list containing all info associated with that ID
        """
        with open(file_name, 'r') as file:
                str_to_find = '!!' + id.strip() # string to look for in the id file
                file_lines = file.readlines()
                for line in file_lines:
                    if str_to_find in line: # if line contains ID, immediately returns list containing that info
                        return [i.strip() for i in line.split('~')[1].split('/')] 
        
        # If no object matching ID is found.
        raise ValueError(f"No object with ID ({id.strip()}) was found in file ({file_name})")
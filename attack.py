from file_id_interpreter import FileIdInterpreter

class Attack:
    """Class representing an attack.

    Attributes:
        name (int): Name of attack
        power (int): Power of attack
        accuracy (int): Accuracy of attack, out of 100.
        range (int): Number of squares 
    """

    # Attributes
    __name = None
    __power = None
    __accuracy = None
    __range = None

    # Constructor
    def __init__(self, attack_id: str):
        # Getting and unpacking file info
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/attack_id.txt', attack_id) # [name, power, accuracy, range]
        name, power, accuracy, range = attribute_list # unpacks attribute_list
        power, accuracy, range = [int(i) for i in (power, accuracy, range)] # converts some attributes to integers
        
        # Setting attributes.
        self.setName(name)
        self.setPower(power)
        self.setAccuracy(accuracy)
        self.setRange(range)

    # Getters
    def getName(self):
        return self.__name
    def getPower(self):
        return self.__power
    def getAccuracy(self):
        return self.__accuracy
    def getRange(self):
        return self.__range

    # Setters
    def setName(self, name):
        self.__name = name
    def setPower(self, power):
        self.__power = power
    def setAccuracy(self, accuracy):
        self.__accuracy = accuracy
    def setRange(self, range):
        self.__range = range

    def isInRange(self, 
                  self_coords: tuple[int, int],
                  target_coords: tuple[int, int],
                  obstructed_coords: list[tuple[int, int]]) -> bool:
        """Determines if the target_coords are in range of self_coords.

        Checks whether target_coords are within taxicab distance of self_coords,
        and the line between their centres does not contain coords in obstructed_coords.
        Returns True if in range, else returns False.
        """
        pass


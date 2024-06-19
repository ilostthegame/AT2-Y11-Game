from file_id_interpreter import FileIdInterpreter

class Attack:
    """
    A class representing an attack

    Attributes:
        name (int): Name of attack
        power (int): Power of attack
        accuracy (int): Accuracy of attack, out of 100.
        range (int): Number of squares 
        cooldown (int): Number of turns before next use (0 => no cooldown)

    Methods: TODO
        getInfo(self): Returns the info.
    """
    # Attributes
    __name = None
    __power = None
    __accuracy = None
    __range = None
    __cooldown = None

    # Constructor
    def __init__(self, attack_id: str):
        # Getting and unpacking file info
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/attack_id.txt', attack_id) # [name, power, accuracy, range, cooldown]
        name, power, accuracy, range, cooldown = attribute_list # unpacks attribute_list
        power, accuracy, range, cooldown = [int(i) for i in (power, accuracy, range, cooldown)] # converts some attributes to integers
        
        # Initialising attack object.
        self.setName(name)
        self.setPower(power)
        self.setAccuracy(accuracy)
        self.setRange(range)
        self.setCooldown(cooldown)
        
        
    # Getters
    def getName(self):
        return self.__name
    def getPower(self):
        return self.__power
    def getAccuracy(self):
        return self.__accuracy
    def getRange(self):
        return self.__range
    def getCooldown(self):
        return self.__cooldown

    # Setters
    def setName(self, name):
        self.__name = name
    def setPower(self, power):
        self.__power = power
    def setAccuracy(self, accuracy):
        self.__accuracy = accuracy
    def setRange(self, range):
        self.__range = range
    def setCooldown(self, cooldown):
        self.__cooldown = cooldown

from file_id_interpreter import FileIdInterpreter
from math import floor, ceil

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
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/attack_id.txt', attack_id)
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
                  origin_coords: tuple[int, int],
                  target_coords: tuple[int, int],
                  obstructed_coords: list[tuple[int, int]]) -> bool:
        """Determines if the target_coords are in range of self_coords.

        Checks whether target_coords are within taxicab distance of origin_coords,
        and there are no obstructed tiles between them.
        Returns True if in range, else returns False.
        """
        # Checks if the target is not within range.
        if (abs(origin_coords[0] - target_coords[0]) + 
            abs(origin_coords[1] - target_coords[1]) > self.getRange()):
            return False
        # Checks if any tiles between origin and target are obstructed.
        intersected_coords = self.getBetweenCoords(origin_coords, target_coords)
        for coords in intersected_coords:
            if coords in obstructed_coords:
                return False
        return True
    
    def getBetweenCoords(self, 
                         origin_coords: tuple[int, int],
                         target_coords: tuple[int, int]) -> set[tuple[int, int]]:
        """Returns list of tiles in between origin_coords and target_coords.

        Gets all tiles intersected by the line between the centres of the tiles.
        The algorithm is as follows:
        If the origin and target tiles are not vertical of each other:
            1. Calculates the equation of the between centres of origin/target tiles
            2. For each x value in between the origin and target coords, 
            calculate the corresponding y value using the equation.
            3. For both the floor and ceiling of the y value, determines
            the coordinates of the tile(s) the line hit at that point.
            4. Adds a tuple representing those coords to a set.
        Else, if the tiles are vertical, calculation of tiles in between is simple.
        Then it removes the origin and target coords from the set.
        """
        intersected_coords = set() # Set of tiles hit by the line.
        if origin_coords[0] - target_coords[0] != 0: # Ensures gradient is not infinite.
            origin_pixel_coords = self.boardToPixelCoords(origin_coords)
            target_pixel_coords = self.boardToPixelCoords(target_coords)
            gradient, y_intercept = self.calcLine(origin_pixel_coords, target_pixel_coords)
            # Getting the range of x values to check.
            start_value = int(min(origin_pixel_coords[0], target_pixel_coords[0]))
            end_value = int(max(origin_pixel_coords[0], target_pixel_coords[0]))
            # Checking each point on the line.
            for x in range(start_value, end_value):
                y = x * gradient + y_intercept
                intersected_coords.add(self.pixelToBoardCoords((x, floor(y))))
                intersected_coords.add(self.pixelToBoardCoords((x, ceil(y))))

        else: # Handling case where the tiles are vertical from another.
            lower_y_value = min(origin_coords[1], target_coords[1])
            upper_y_value = max(origin_coords[1], target_coords[1])
            for y in range(lower_y_value, upper_y_value+1):
                intersected_coords.add((origin_coords[0], y))

        # Removing origin and target coords from the set.
        try:
            intersected_coords.remove(origin_coords)
            intersected_coords.remove(target_coords)
        except KeyError: # If origin_coords = target_coords.
            pass
        return intersected_coords

    def boardToPixelCoords(self, board_coords: tuple[int, int]) -> tuple[float, float]:
        """Converts board coords to the coords of the centre of the tile.
        
        Note this returns the exact centre of a tile (due to pixel size of tile being even).
        For example, with the topleft-most tile, it will return (31.5, 31.5).
        """
        return (board_coords[0]*64 + 31.5, board_coords[1]*64 + 31.5)
    
    def pixelToBoardCoords(self, pixel_coords: tuple[int, int]) -> tuple[int, int]:
        """Converts board coords to the coords of the centre of the tile."""
        return (floor(pixel_coords[0]/64), floor(pixel_coords[1]/64))
    
    def calcLine(self, 
                 coords1: tuple[float, float], 
                 coords2: tuple[float, float]) -> tuple[float, float]:
        """Returns (gradient, y_intercept) of line through coords1, coords2."""
        gradient = (coords1[1]-coords2[1]) / (coords1[0]-coords2[0])
        y_intercept = coords1[1] - gradient*coords1[0]
        return (gradient, y_intercept)
    

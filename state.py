from enum import Enum
from copy import deepcopy

""" Enumeration to represents the possible movement directions"""
class Directions(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

""" State represents a game of taquin : obligatory of dimension 3x3 """
class State:
    """ Initialisation of the state. Takes only a 2D array in parameters, the other attributes don't need to be set here."""
    def __init__(self, state):
        self.current_state = state
        self.operations = [Directions.Up,
                           Directions.Down,
                           Directions.Left,
                           Directions.Right]

        self.parent = None

    """ Allows to iterate over the 2D array of a state"""
    def __iter__(self):
        for item in self.current_state:
            yield item

    """Allows to print an object"""
    def __str__(self):
        return "[%s]" % ", ".join(map(str, self.current_state))

    """Allows the deepcopy of an object"""
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)

        result.operations = deepcopy(self.operations)
        result.current_state = deepcopy(self.current_state)

        return result

    """ Allows to compare to state. Permits to use the in operator"""
    def __eq__(self, other):
        return self.current_state == other.current_state

    """ Getter for the parent attribute"""
    def __parent__(self):
        return self.parent

    """ Defines if the state is legal. It always is in our case."""
    def legal(self):
        return True

    """Return the operators whose applicable according of the row and column position"""
    def define_operations(self, zero_row, zero_column):
        applicable_operators = []

        # It could be better to use a dictionnary to map functions. Switch doesn't exists in python
        # Then we test in the columnt
        if zero_column == 0:
            applicable_operators.append(Directions.Right)
        elif zero_column == 1:
            applicable_operators.append(Directions.Left)
            applicable_operators.append(Directions.Right)
        elif zero_column == 2:
            applicable_operators.append(Directions.Left)

        # We test the position of the zero in the rows
        if zero_row == 0:
            applicable_operators.append(Directions.Down)
        elif zero_row == 1:
            applicable_operators.append(Directions.Up)
            applicable_operators.append(Directions.Down)    
        elif zero_row == 2:
            applicable_operators.append(Directions.Up)

        return applicable_operators

    """Parse and find the state to find and return row and column index of the zero"""
    def find_zero_location(self):
        zero_found = False;
        current_row = 0;
        current_column = 0;

        # decomposation of the 2D
        while not zero_found and current_row < 3:
            if current_column == 3:
                current_column = 0
                current_row += 1

            zero_found = self.current_state[current_row][current_column] == 0
            if not zero_found:
                current_column += 1

        return current_row, current_column

    """Determinate the available operators of the state"""
    def applicable_operations(self):
        zero_row, zero_column = self.find_zero_location()
        return self.define_operations(zero_row, zero_column)

    """Applies an operation to the state. Returns a new state, we don't apply on the given state"""
    def apply_operation(self, operation):
        zero_row, zero_column = self.find_zero_location()
        new_state = deepcopy(self)
        new_state.parent = self

        # Swap operations. May not be the best way to do it, but works fine
        if operation == Directions.Up:
            new_state.current_state[zero_row][zero_column] = new_state.current_state[zero_row - 1][zero_column]
            new_state.current_state[zero_row - 1][zero_column] = 0

        if operation == Directions.Down:
            new_state.current_state[zero_row][zero_column] = new_state.current_state[zero_row + 1][zero_column]
            new_state.current_state[zero_row + 1][zero_column] = 0

        if operation == Directions.Left:
            new_state.current_state[zero_row][zero_column] = new_state.current_state[zero_row][zero_column - 1]
            new_state.current_state[zero_row][zero_column - 1] = 0

        if operation == Directions.Right:
            new_state.current_state[zero_row][zero_column] = new_state.current_state[zero_row][zero_column + 1]
            new_state.current_state[zero_row][zero_column + 1] = 0

        return new_state

    """Defines if the state is a final state. The final state rule could be changed here"""
    def final(self):
        #print("Final : ", self.current_state == [[0,1,2], [3,4,5],[6,7,8]])
        return self.current_state == [[0,1,2],
                                      [3,4,5],
                                      [6,7,8]]

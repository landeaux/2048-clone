"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
   
    def move(old_line):
        """
        Function that iterates over the input and creates an output
        list that has all of the non-zero tiles slid over to the 
        beginning of the list with the appropriate number of zeroes 
        at the end of the list.
        """
        result_line = [0] * len(old_line)
        for tile in range(len(old_line)):
            if old_line[tile] > 0:
                for result_tile in range(len(result_line)):
                    if result_line[result_tile] == 0:
                        result_line[result_tile] = old_line[tile]
                        break
        return result_line

    def combine(result_line):
        """
        Function that iterates over the list created in the move() 
        function and creates another new list in which pairs of tiles 
        in the first list are replaced with a tile of twice the value 
        and a zero tile.
        """
        for result_tile in range(len(result_line)-1):
            if result_line[result_tile] == result_line[result_tile+1]:
                result_line[result_tile] += result_line[result_tile+1]
                result_line[result_tile+1] = 0
        return result_line
    
    return move(combine(move(line)))

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = []
        
        # creates dict using direction values as the keys 
        # and uses list comprehensions to pre-compute the 
        # correspinging lists of initial tiles
        self._initial_tiles = \
            {UP: [(0, col) for col in range(self._grid_width)], 
             DOWN: [(self._grid_height-1, col) for col in range(self._grid_width)], 
             LEFT: [(row, 0) for row in range(self._grid_height)], 
             RIGHT: [(row, self._grid_width-1) for row in range(self._grid_height)]}
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)] 
                     for dummy_row in range(self._grid_height)]
        
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_str = ""
        for row in self._grid:
            grid_str += str(row) + "\n"

        return grid_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction < 3:
            length = self._grid_height
        else:
            length = self._grid_width
        
        indices = []
        lists_to_move = []
        
        # Creates a list of lists containing indices of tiles
        # to be merged. Gets indices for each tile 
        # by multiplying the OFFSETS value by number from 0 
        # to the length of the row or column - 1, then adds 
        # that value to the indices of the initial tile.
        for tile in self._initial_tiles[direction]:
            indices.append([(tile[0] + OFFSETS[direction][0] * i, 
                        tile[1] + OFFSETS[direction][1] * i) 
                            for i in range(length)])
            
        # lists_to_move is appended with lists containing
        # the values of each tile to be merged by iterating
        # thru the indices list, calling self._get_tile on
        # the indices, and storing that value in the list.
        # This is done for each row or column to be merged
        for index_list in indices:
            lists_to_move.append([self.get_tile(index[0], index[1]) for index in index_list])
        
        merged_lists = []
        
        for item in lists_to_move:
            merged_lists.append(merge(item))
        
        for index_i in range(len(merged_lists)):
            for index_j in range(len(merged_lists[index_i])):
                self.set_tile(indices[index_i][index_j][0], 
                              indices[index_i][index_j][1], 
                              merged_lists[index_i][index_j])
        
        if merged_lists != lists_to_move:
            self.new_tile()
        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_squares = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._grid[row][col] == 0:
                    empty_squares.append((row,col))

        rand_square = random.choice(empty_squares)
        
        rand_num = random.randrange(0, 100)
        
        if 10 <= rand_num and rand_num < 100:
            pick = 2
        else: 
            pick = 4
        
        self.set_tile(rand_square[0], rand_square[1], pick)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 5))
from board_to_graph import (Corner4, Corner3V1, 
                            Corner3V2, Corner3V3, Corner3V4, Corner2V1, Corner2V2, Corner2V3, 
                            Corner2V4, Corner2V5, Corner2V6, Corner1V1, Corner1V2, Corner1V3, Corner1V4)
from print_board import display_board
from board_to_graph import knights_graph
from build_grid_graph import randomized_grid_graph
from pprint import pprint
from Utils.utlities import (print_matrix, rotate180, transpose, print_chessboard_mapping)


# From a grid graph, create the corresponding chessboard (reduction).
# grid graph is an adjacency list of (x,y) tuples.

def grid_graph_to_chessboard(G, M):
    """
    G: adjacency list of a grid graph { (x,y): [(x2,y2), ...], ... }
    M: dictionary mapping 4-bit strings "b1b2b3b4" to values

    Returns a dictionary { (x,y): M[b1b2b3b4] }
    """
    
    # Unit direction vectors in the order (up, right, down, left)
    directions = [
        (0, 1),   # up
        (1, 0),   # right
        (0, -1),  # down
        (-1, 0)   # left
    ]
    
    result = {}

    xs = [x for (x, y) in G.keys()]
    ys = [y for (x, y) in G.keys()]

    width  = max(xs) + 1
    height = max(ys) + 1

    for (x, y), neighbors in G.items():

        bitstring = ""

        b_top = "1"
        b_bottom = "1"
        b_right = "1"
        b_left = "1"

        if (x + y) % 2 == 0:

            b_top =     "1" if (x, y-1) in neighbors else "0"
            b_right =   "1" if (x+1, y) in neighbors else "0"
            b_bottom =  "1" if (x, y+1) in neighbors else "0"
            b_left =    "1" if (x-1, y) in neighbors else "0"
            
            bitstring = b_top + b_right + b_bottom + b_left
            index = int(bitstring, 2)

            if index != 0:
                if y == 0:
                    b_top = "1"
                if y == height - 1:
                    b_bottom = "1"
                if x == 0:
                    b_left = "1"
                if x == width - 1:
                    b_right = "1"

        else:
            
            b_top =     "1" if (x+1, y) in neighbors else "0"
            b_right =   "1" if (x, y-1) in neighbors else "0"
            b_bottom =  "1" if (x-1, y) in neighbors else "0"
            b_left =    "1" if (x, y+1) in neighbors else "0"

            bitstring = b_top + b_right + b_bottom + b_left
            index = int(bitstring, 2)

            if index != 0:
                if y == 0:
                    b_right = "1"
                if y == height - 1:
                    b_left = "1"
                if x == 0:
                    b_bottom = "1"
                if x == width - 1:
                    b_top = "1"

        bitstring = b_top + b_right + b_bottom + b_left
        index = int(bitstring, 2)

        # Look up M[bitstring]
        board = M[index]
        if (x + y) % 2 == 1:
            board = transpose(rotate180(board))

        result[(x, y)] = board

    return result

'''
    Given the grid graph and the chessboards, it tiles the chessboards up into
    one big chessboard.
'''
def glue_chessboards(result, tile_size):
    # result: dict {(x,y): 9x9 matrix}

    xs = [x for (x, y) in result.keys()]
    ys = [y for (x, y) in result.keys()]

    width  = max(xs) + 1
    height = max(ys) + 1

    final = [[0] * (width * tile_size) for _ in range(height * tile_size)]

    for (x, y), tile in result.items():
        base_x = x * tile_size
        base_y = y * tile_size

        for i in range(tile_size):
            for j in range(tile_size):
                final[base_y + j][base_x + i] = tile[j][i]

    return final


if __name__ == "__main__":
    # All possible chessboards that can be mapped (IN BINARY)
    ''' 
    (1,_,_,_) left edge
    (_,1,_,_) bottom edge
    (_,_,1,_) right edge
    (_,_,_,1) top edge
    '''

    Corner0 = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        ]
    # Skip entry 0
    Boards = [
        Corner0,
        Corner1V2, #(0,0,0,1),
        Corner1V3, #(0,0,1,0),
        Corner2V4, #(0,0,1,1),
        Corner1V4, #(0,1,0,0),
        Corner2V5, #(0,1,0,1),
        Corner2V1, #(0,1,1,0),
        Corner3V1, #(0,1,1,1),
        Corner1V1, #(1,0,0,0),
        Corner2V6, #(1,0,0,1),
        Corner2V2, #(1,0,1,0),
        Corner3V4, #(1,0,1,1),
        Corner2V3, #(1,1,0,0),
        Corner3V3, #(1,1,0,1),
        Corner3V2, #(1,1,1,0),
        Corner4  #(1,1,1,1)
    ]

    # feel free to add any holes you want
    holes = {}
    G = randomized_grid_graph(6, 6, p=0.5, holes=None)

    mapped = grid_graph_to_chessboard(G, Boards)
    print_chessboard_mapping(mapped)
    combined_board = glue_chessboards(mapped, 9)
    # print_matrix(combined_board)
    pprint(G)
    display_board(combined_board, 6*9, 6*9)

    '''
    print_matrix(Corner4)
    print('\n\n')
    print_matrix(flip_horizontal(Corner4))

    display_board(Corner4,9,9)
    display_board(rotate90_clockwise(Corner4), 9,9)
    #display_board(flip_vertical(flip_horizontal(Corner4)), 9,9)
    '''
    '''
    print("\n\n")
    print(knights_graph(mapped[(0,1)]))
    '''

    '''
    print_matrix(Corner4)
    goal = [
        [0,1,0,0,0,0,0,0,0],
        [0,1,0,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,1,0],
    ]
    print("\n\n")
    print_matrix(rotate180(Corner4))
    print('\n\n')
    print_matrix(transpose(rotate180(Corner4)))
    print('\n\n')
    print("now moving onto Corner2V1 \n\n")
    print_matrix(Corner2V1)
    print('\n\n')
    print_matrix(transpose(rotate180(Corner2V1)))
    '''

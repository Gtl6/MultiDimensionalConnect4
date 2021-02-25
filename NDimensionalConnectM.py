# 2-player N dimensional Connect M
# A project by Griffin Lynch
# Ever feel like Connect 4 is just a little too easy?
# Put out by the fact that mathematicians have already "solved" it?
# Have I got the game for you! Increase the dimensionality and
#   resultant string length. Everything you need in a Connect M game!

import sys

WIN_LEN = 4 # How long the string needs to be for a player to win... should be at least 1, and definitely at most as long as the longest stretch on the board
            # But I'm not going to check the game is winnable for you. If you set the parameters for an unwinnable game, don't come crying to me when nobody wins

# Add dimensions as needed, 2 is the minimum
# Note as you increase the dimensionality of the list, the computation required to check all lines grows exponentially
BOARD_DIMENSIONS = [7, 6, 4] 


# We'll call this number N in the comments
DIMENSIONALITY = len(BOARD_DIMENSIONS)

# The visual representation of the players' tokens
PLAYER_TOKENS = ['*', '+']


# The amount of available slots will be the product of the dimensions
boardLen = 1
for i in BOARD_DIMENSIONS:
    if i != 0:
        boardLen *= i

board = ['_'] * boardLen

# This function will calculate how much space one board of DIM - 1 takes up
#   DIM is a natural integer
#   So say BOARD_DIMENSIONS = [7, 6, 4]
#   DIM = 0 will return 1
#   DIM = 1 will return 7
#   DIM = 2 will return 42
#   DIM = 3 is undefined
# Used to calculate the position of something within a list
def get_lower_widths(DIM):
    width = 1
    for i in range(0, DIM):
        width *= BOARD_DIMENSIONS[i]

    return width

# This function will let us index into the board at a specific position
#   pos is an N-length list of Natural integers
def get_offset(pos):
    offset = 0
    for dimension in range(0, DIMENSIONALITY):
        offset += pos[dimension] * get_lower_widths(dimension)

    return offset

# This function will let us get something from the board using a position var
#   pos is an N-length list of Natural integers
def get_item(pos):
    if len(pos) != DIMENSIONALITY:
        print("ERROR: list given to get_item of length " + str(len(pos)))

    return board[get_offset(pos)]

# This function will let us add a stone to the board using a position var
#   pos is an N-length list of Natural integers
#   item is a player's item, either + or *
#   it will not check if the spot is already set, so make sure you check it beforehand
def set_item(pos, item):
    if len(pos) != DIMENSIONALITY:
        print("ERROR: list given to set_item of length " + str(len(pos)))
    offset = get_offset(pos)
    board[offset] = item

# This function will drop a stone into the lowest position in the board
#   at the point specified
#   pos is an (N - 1) length list of Natural integers (y coord is excluded)
#       because the stone will drop to the lowest available y
#       if that y-plane is already full, it will return False
#       if successful, it will return the coordinates of the dropped stone
def drop_stone(pos, item):
    #Start at the bottom and go up
    for i in range(0, BOARD_DIMENSIONS[1]):
        position = pos.copy()
        # stick the y-value in
        position.insert(1, i)
        value = get_item(position)
        # If the spot is empty, place the stone and return the position
        if value == '_':
            set_item(position, item)
            return position
    #If the loop terminates, then the column is full
    return False


# Calculates the offset of a particular board within the list, based on the dimensions list
def calculate_2D_offset(dimension_list):
    offset = 0

    # The 2D case is easy, there's only one board
    #   technically this happens implicitly anyway with the code I've written below, but better to be explicit
    if len(dimension_list) == 0:
        return offset
    
    for i in range(2, DIMENSIONALITY):
        offset += dimension_list[i - 2] * get_lower_widths(i)

    return offset
        

# Allows the player to see a 2-dimensional slice of the N-dimensional board
#   Will this be helpful? Probably not. But I feel like I should include it
def run_look_function():
    dim_list = []
    for i in range(2, DIMENSIONALITY):
        while(True):
            print("Please enter a number in [0, " + str(BOARD_DIMENSIONS[i] - 1) + "] for the " + str(i + 1) + " dimension.")
            given_no = int(input())
            if given_no < BOARD_DIMENSIONS[i] and given_no > -1:
                dim_list.append(given_no)
                break
            # If it isn't a good number, repeat the prompt
            print("That number is not well formatted")

    print("Showing the 2D slice: [x, y", end='')
    for i in dim_list:
        print(", " + str(i), end='')
    print("]")

    # First do the numbers at the top of the board
    for i in range(0, BOARD_DIMENSIONS[0]):
        print(' ' + str(i), end='')
    print()
        
    # Find where our data is
    offset = calculate_2D_offset(dim_list)

    # Then print out our board
    board_print = ""
    for i in range(0, BOARD_DIMENSIONS[1]):
        board_line = ""
        for j in range(0, BOARD_DIMENSIONS[0]):
            board_line += '|' + board[offset]
            offset += 1
        # End the line
        board_print = board_line + "|\n" + board_print

    # Print it
    print(board_print)

# Checks to see if all elements in a list are at least 0
def all_elements_natural(my_list):
    for i in my_list:
        if i < 0:
            return False

    return True

# Checks to see if all elements in a list are below their length specified in the board dimensions
def all_elements_within_limits(my_list):
    for i in range(0, len(my_list)):
        if my_list[i] >= BOARD_DIMENSIONS[i]:
            return False

    return True

# Adds together two vectors by adding each of their indices. Pretty standard stuff.
#   Make sure they're the same length, the behavior if they aren't is undefined
#   They need to be vectors of integers
def vector_add(vec1, vec2):
    for i in range(0, len(vec1)):
        vec1[i] = vec1[i] + vec2[i]

    return vec1

# checks to see if there are any strings of length WIN_LEN with the new piece in it across all dimensions
# Does this by generating all N-length binary strings, and treating them as directional vectors to check along
#   You'll just have to trust me that this works and is exhaustive of all possible directions
def check_player_won(drop_result, player):
    player_stone = get_item(drop_result)

    # Don't want to use the number 0 because the 0 vector doesn't have a direction
    for i in range(1, 2 ** DIMENSIONALITY):
        # Get the binary string
        direction = str(format(i, 'b'))
        direction = list(direction) # cast it to a list
        for j in range(0, DIMENSIONALITY - len(direction)): # pad out the front with 0's
            direction.insert(0, '0')

        # Now change all the items back to numbers and multiply by -1
        #   We do this because we'll move backwards along the direction first, then count moving forwards
        #   Made this a function because I do it again in a couple lines
        def flip_direction():
            for i in range(0, len(direction)):
                direction[i] = int(direction[i]) * -1

        flip_direction()

        looking_at = drop_result.copy()
        # Move backwards along the vector for as long as the same stone occurs (and we're still on the board)
        while all_elements_natural(looking_at) and get_item(looking_at) == player_stone:
            looking_at = vector_add(looking_at, direction)

        # When that loop terminates, we're either not on a player stone or off the board, so flip the vector and move forwards once
        flip_direction()
        looking_at = vector_add(looking_at, direction)

        count = 0
        # Loop is pretty similar to the previous one, except we'll be counting how long the string is this time
        while all_elements_within_limits(looking_at) and get_item(looking_at) == player_stone:
            count += 1
            looking_at = vector_add(looking_at, direction)

        if count >= WIN_LEN:
            print("Player " + str(player) + " has won! Congratulations!")
            sys.exit()

        #Otherwise just keep checking other directions
    # If we got to the end of the loop, the player didn't win
            
    

# Just lets a player drop a stone into the board, which then falls to the lowest free y-value in that column
def run_drop_function(player):
    dim_list = []
    for i in range(0, DIMENSIONALITY):
        # Can't select a y-value
        if i == 1:
            continue
        while(True):
                print("Please enter a number in the range [0, " + str(BOARD_DIMENSIONS[i] - 1) + "] for the " + str(i + 1) + " dimension's coordinate.")
                given_no = int(input())
                if given_no < BOARD_DIMENSIONS[i] and given_no > -1:
                    dim_list.append(given_no)
                    break
                # If it isn't a good number, repeat the prompt
                print("That number is not well formatted")

    # Now that we have a drop position, we can drop it
    item = PLAYER_TOKENS[player - 1]
    drop_result = drop_stone(dim_list, item)

    # If it doesn't work, the column was full
    if drop_result == False:
        print("Unfortunately that y-column is full. Returning to the main loop...")
        return False
    else:
        # Otherwise we have to check to see if that player just won
        check_player_won(drop_result, player)
        return True
    
        
# This creates a string rep of the board's dimensions
def board_dim_string():
    board_string = ""
    for i in BOARD_DIMENSIONS:
        board_string += str(i) + "x"

    board_string = board_string[:-1]
    return board_string

# Now let's get to the actual game code
print("Hello! Welcome to a game of Connect-" + str(WIN_LEN) + "!")
print("The game takes place on a " + board_dim_string() + " board")
print("As such, each player will be expected to give a " + str(DIMENSIONALITY - 1) + " length string.")
print("The stone will automatically drop to the lowest possible y-value")
print("Good luck!")

# Our game loop
player = 1
while True:
    print("\n\nPlayer " + str(player) + ", what would you like to do?")
    print("> ", end="")
    in_string = input().lower()
    if in_string == "help":
        print("Available commands: help, look, drop, quit")
    elif in_string == "quit":
        print("Thanks for playing!")
        sys.exit()
    elif in_string == "look":
        run_look_function()
    elif in_string == "drop":
        did_it_work = run_drop_function(player)
        # If it didn't work we can just loop again
        #   Otherwise switch which player is playing
        if did_it_work:
            if player == 1:
                player = 2
                continue
            else:
                player = 1
                continue
        




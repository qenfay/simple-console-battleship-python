# References:
# https://en.wikipedia.org/wiki/Battleship_(game)
# https://www.datagenetics.com/blog/december32011/


import random
from queue import LifoQueue

# Dictionary of ships and their corresponding sizes
ships = {'Carrier': 5, 'Battleship': 4, 'Destroyer': 3, 'Submarine': 3, 'Patrol Boat': 2}
DIMENSION = 10

mode = "hunt"
stack = LifoQueue()  # coordinates stack for the generate_cpu_hit function


def generate_cpu_hit(prev_x, prev_y, cpu_main_board):
    if mode == "hunt":
        if stack.empty() == False:
            return stack.get()
        else:
            hit_coord = [random.randint(1, DIMENSION), random.randint(1, DIMENSION)]
            while (cpu_main_board[hit_coord[0] - 1][hit_coord[1] - 1] != '-'):
                hit_coord = [random.randint(1, DIMENSION), random.randint(1, DIMENSION)]
            return hit_coord
    elif mode == "target":
        # Edge cases
        if (prev_x == 1 or prev_y == 1 or prev_y == DIMENSION or prev_x == DIMENSION):
            # First row
            if (prev_x == 1):
                if (cpu_main_board[prev_x - 1 + 1][prev_y - 1] != 'X'):
                    # Try aiming south
                    stack.put([prev_x + 1, prev_y])

                if (prev_y == 1 or prev_y == DIMENSION):
                    # First column
                    if (prev_y == 1 and cpu_main_board[prev_x - 1][prev_y - 1 + 1] != 'X'):
                        # Try aiming east
                        stack.put([prev_x, prev_y + 1])

                    # Last column
                    elif (prev_y == DIMENSION and cpu_main_board[prev_x - 1][prev_y - 1 - 1] != 'X'):
                        # Try aiming west
                        stack.put([prev_x, prev_y - 1])

                if (prev_y > 1 and prev_y < DIMENSION):
                    # 2nd to (DIMENSION - 1)th column

                    # Try aiming south
                    if (cpu_main_board[prev_x - 1 + 1][prev_y - 1] != 'X'):
                        stack.put([prev_x + 1, prev_y])
                    # Try aiming east
                    if (cpu_main_board[prev_x - 1][prev_y - 1 + 1] != 'X'):
                        stack.put([prev_x, prev_y + 1])
                    # Try aiming west
                    if (cpu_main_board[prev_x - 1][prev_y - 1 - 1] != 'X'):
                        stack.put([prev_x, prev_y - 1])

            # First column
            elif (prev_y == 1):
                if (cpu_main_board[prev_x - 1][prev_y - 1 + 1] != 'X'):
                    # Try aiming east
                    stack.put([prev_x, prev_y + 1])

                    if (prev_x > 1 and prev_x < DIMENSION):
                        # 2nd to (DIMENSION - 1) rows
                        if (cpu_main_board[prev_x - 1 + 1][prev_y - 1] != 'X'):
                            # Try aiming south
                            stack.put([prev_x + 1, prev_y])

                        if (cpu_main_board[prev_x - 1 - 1][prev_y - 1] != 'X'):
                            # Try aiming north
                            stack.put([prev_x - 1, prev_y])

            # Last row
            elif (prev_x == DIMENSION):
                if (cpu_main_board[prev_x - 1 - 1][prev_y - 1] != 'X'):
                    # Try aiming north
                    stack.put([prev_x - 1, prev_y])

                # 2nd to (DIMENSION - 1)th columns
                if (prev_y > 1 and prev_y < DIMENSION):

                    if (cpu_main_board[prev_x - 1][prev_y - 1 + 1] != 'X'):
                        # Try aiming east
                        stack.put([prev_x, prev_y + 1])

                    if (cpu_main_board[prev_x - 1][prev_y - 1 - 1] != 'X'):
                        # Try aiming west
                        stack.put([prev_x, prev_y - 1])

            # Last column
            else:
                # 2nd to (DIMENSION - 1)th rows
                if (prev_x > 1 and prev_x < DIMENSION):
                    # Try aiming north
                    if (cpu_main_board[prev_x - 1 - 1][prev_y - 1] != 'X'):
                        stack.put([prev_x - 1, prev_y])
                    # Try aiming south
                    if (cpu_main_board[prev_x - 1 + 1][prev_y - 1] != 'X'):
                        stack.put([prev_x + 1, prev_y])
                    # Try aiming west
                    if (cpu_main_board[prev_x - 1][prev_y - 1 - 1] != 'X'):
                        stack.put([prev_x, prev_y - 1])


        else:
            # Try aiming north
            if (cpu_main_board[prev_x - 1 - 1][prev_y - 1] != 'X'):
                stack.put([prev_x - 1, prev_y])
            # Try aiming south
            if (cpu_main_board[prev_x - 1 + 1][prev_y - 1] != 'X'):
                stack.put([prev_x + 1, prev_y])
            # Try aiming east
            if (cpu_main_board[prev_x - 1][prev_y - 1 + 1] != 'X'):
                stack.put([prev_x, prev_y + 1])
            # Try aiming west
            if (cpu_main_board[prev_x - 1][prev_y - 1 - 1] != 'X'):
                stack.put([prev_x, prev_y - 1])

        return stack.get()


# Function to initialize the given board
def init_board(board):
    for i in range(DIMENSION):
        board.append(['-'] * DIMENSION)


# Function to print the given board along with the player's name
def print_board(board, player_name, additional_text):
    print("\n{}'s {} board : ".format(player_name, additional_text))
    for row in board:
        print(" ".join(row))


def is_ship_placeable(board, row, col, orientation, ship_length):
    flag = True

    i = 0
    if (orientation == 'H'):
        while ((i < ship_length) and flag):
            if (board[row][col + i] != '-'):
                flag = False
            i += 1

    elif (orientation == 'V'):
        while ((i < ship_length) and flag):
            if (board[row + i][col] != '-'):
                flag = False
            i += 1

    return flag


# Function to generate cpu's ships
def generate_cpu_ships(board):
    orientations = ['H', 'V']
    for ship_name, ship_length in ships.items():
        # [DEBUG ----]
        # print_board(board,"CPU","")
        # print("\nGenerating starting coordinates for the {} ship (length {})".format(ship_name,ship_length))
        # [---- DEBUG]
        flag = 1

        # Continue attempting to place ship until succesful
        while (flag):
            # Generate row and column randomly
            row = random.randint(0, 9)
            col = random.randint(0, 9)

            # Pick orientation randomly
            orientation = orientations[random.randint(0, 1)]

            i = 0
            if ((orientation == 'H') and (board[row][col] == '-') and (
                    (col + ship_length) <= DIMENSION)):  # Check bounds and ensure that location is empty
                if (is_ship_placeable(board, row, col, orientation, ship_length)):  # Ensure that ships don't overlap
                    flag = 0  # Ship placed successfully
                    # [DEBUG ----]
                    # print("Generated coordinates : [{}][{}], orientation : {}".format(row + 1,col + 1,orientation))
                    # [---- DEBUG]
                    while (i < ship_length):
                        board[row][col + i] = 'S'
                        i += 1


            elif ((orientation == 'V') and (board[row][col] == '-') and (
                    (row + ship_length) <= DIMENSION)):  # Check bounds and ensure that location is empty
                if (is_ship_placeable(board, row, col, orientation, ship_length)):  # Ensure that ships don't overlap
                    flag = 0  # Ship placed successfully
                    # [DEBUG ----]
                    # print("Generated coordinates : [{}][{}], orientation : {}".format(row,col,orientation))
                    # [---- DEBUG]
                    while (i < ship_length):
                        board[row + i][col] = 'S'
                        i += 1


def input_coordinate(coordinate, message):
    flag = 1
    while (flag):
        try:
            print("{} the {} (1-{}) : ".format(message, coordinate, DIMENSION), end='')
            value = int(input())
            if (value < 1 or value > DIMENSION):
                print(
                    "Invalid {} number. Must be on the grid (between 1-{}). Try again!\n".format(coordinate, DIMENSION))

            else:
                flag = 0

        except ValueError:
            print("Invalid input. Must be an integer!\n")

    return value


def input_orientation():
    flag = 1
    while (flag):

        orientation = input("Enter orientation (H for horizontal, V for vertical) : ").upper()

        if not (orientation == "H" or orientation == "V"):
            print("Invalid orientation. Must be either H or V.Try again!\n")

        else:
            flag = 0

    return orientation


# Function to allow the player to place their ships
def place_ships(board, player_name):
    # Iterate over the ships list
    for ship_name, ship_length in ships.items():
        print_board(board, player_name, "Ship")
        flag = 1

        # Continue attempting to place ship until successful
        while (flag):
            print("\nEnter starting coordinates for the {} ship (length {})".format(ship_name, ship_length))
            row = input_coordinate("row", "Enter") - 1
            col = input_coordinate("column", "Enter") - 1
            orientation = input_orientation()

            i = 0

            if (orientation == 'H'):  # Check bounds and ensure that location is empty

                if ((board[row][col] == '-') and ((col + ship_length) <= DIMENSION)):

                    if (
                            is_ship_placeable(board, row, col, orientation,
                                              ship_length)):  # Ensure that ships don't overlap
                        flag = 0  # Ship placed successfully
                        while (i < ship_length):
                            board[row][col + i] = 'S'
                            i += 1
                    else:
                        print("Invalid coordinates: Unable to place ship because of overlapping. Try again!")

                elif (board[row][col] != '-'):
                    print("Invalid coordinates: Unable to place ship because of overlapping. Try again!")

                else:
                    print("Invalid coordinates: Unable to place ship because it won't fit on the grid. Try again!")


            elif (orientation == 'V'):  # Check bounds and ensure that location is empty
                if ((board[row][col] == '-') and ((row + ship_length) <= DIMENSION)):

                    if (
                            is_ship_placeable(board, row, col, orientation,
                                              ship_length)):  # Ensure that ships don't overlap
                        flag = 0  # Ship placed successfully
                        while (i < ship_length):
                            board[row + i][col] = 'S'
                            i += 1
                    else:
                        print("Invalid coordinates: Unable to place ship because of overlapping. Try again!")

                elif (board[row][col] != '-'):
                    print("Invalid coordinates: Unable to place ship because of overlapping. Try again!")

                else:
                    print("Invalid coordinates: Unable to place ship because it won't fit on the grid. Try again!")


def hit(guess_x, guess_y, ship_board, main_board):
    # error catching
    if (not (0 <= guess_x <= (DIMENSION - 1))) or (not (0 <= guess_y <= (DIMENSION - 1))):
        return -1

    # the two arrays must be 2D boolean of equal dimensions
    # guess_x and guess_y are integers of coordinates
    if ship_board[guess_x][guess_y] == 'S':
        # Hit!
        main_board[guess_x][guess_y] = 'X'
        ship_board[guess_x][guess_y] = 'H'  # sunk ship
        return 1
    elif ship_board[guess_x][guess_y] == '-':
        # Miss!
        main_board[guess_x][guess_y] = 'O'
        return 0
    elif ship_board[guess_x][guess_y] == 'H':
        # Already Sunk!
        return 2


if __name__ == "__main__":

    cpu_main_board = []
    cpu_ship_board = []
    player_main_board = []
    player_ship_board = []
    game_over = False

    init_board(cpu_ship_board)
    init_board(player_main_board)
    init_board(player_ship_board)
    init_board(cpu_main_board)

    cpu_hit_coordinates = [1, 1]

    player_name = str(input("Enter your name: "))

    print_board(player_main_board, player_name, "Main")
    print_board(player_main_board, player_name, "Ship")

    # generate cpu ships
    generate_cpu_ships(cpu_ship_board)

    # [DEBUG ----]
    # print_board(cpu_ship_board, "CPU", "Ship [CHEATING!]")
    # [---- DEBUG]

    # ask user to place ships
    print("#### You must now place your ships on your ship board ####")
    place_ships(player_ship_board, player_name)
    print_board(player_ship_board, player_name, "Ship")

    remaining_cpu_ships = 17
    remaining_player_ships = 17
    print_board(player_main_board, player_name, "Main")

    while not (game_over):

        # let the user guess
        guess_x = input_coordinate("row", "Guess")
        guess_y = input_coordinate("column", "Guess")


        # hit the guesses
        hit_result = hit(guess_x - 1, guess_y - 1, cpu_ship_board, player_main_board)

        if hit_result == 1:
            print("Hit! You have sunk a chunk of a battleship\n")
            remaining_cpu_ships -= 1
        elif hit_result == 0:
            print("Miss! You shot into the ocean :(\n")
        elif hit_result == -1:
            print("Your coordinates are out of bounds. Do you even know what you're doing?\n")
            continue
        elif hit_result == 2:
            print("Already hit this target!")
            continue

        print_board(player_main_board, player_name, "Main")

        # let cpu hit
        cpu_hit_coordinates = generate_cpu_hit(cpu_hit_coordinates[0], cpu_hit_coordinates[1], cpu_main_board)
        cpu_hit_result = hit(cpu_hit_coordinates[0] - 1, cpu_hit_coordinates[1] - 1, player_ship_board, cpu_main_board)
        if cpu_hit_result == 1:
            print("Hit! The computer has sunk a chunk of your ships!\n")
            mode = "target"
            remaining_player_ships -= 1
        elif cpu_hit_result == 0 or cpu_hit_result == 2:
            print("Miss! The computer has fortunately shot into the ocean! :)\n")
            mode = "hunt"

        # show the player their ship board
        print_board(player_ship_board, player_name, "Ship")

        # [DEBUG ----]
        # print_board(cpu_main_board, "CPU", "Main")
        # [---- DEBUG]
        # check if game over
        if remaining_cpu_ships <= 0 or remaining_player_ships <= 0:
            game_over = True

    print("Game is done!\n")
    if remaining_cpu_ships == 0:
        print("You win!")
    elif remaining_player_ships == 0:
        print("You lose!")

    print("\nHere's how the CPU did!\n----------------")
    print_board(cpu_main_board, "CPU", "Main")
    print_board(cpu_ship_board, "CPU", "Ship")

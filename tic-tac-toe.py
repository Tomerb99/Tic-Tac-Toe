import turtle as t
import random as r
import pickle as p

# a dict that contains coordinates for winning line
frame_line = {(1, 1): (-100, 150), (1, 2): (0, 150), (1, 3): (100, 150),
              (2, 1): (-100, 50), (2, 2): (0, 50), (2, 3): (100, 50),
              (3, 1): (-100, -50), (3, 2): (0, -50), (3, 3): (100, -50)}

# save last game file
SAVE_FILE = 'tictactoe_save.pkl'
# history file score
HISTORY_FILE = 'tictactoe_history.csv'

# default game state variables
turn = 0
player_symbol = None
computer_symbol = None
level = '1'

# default player names (will be set during setup)
name_cross = 'Cross'
name_circle = 'Circle'
name_human = 'Player'
name_computer = 'Computer'


def tic_tac_toe():
    """function to draw tic tac toe board"""
    t.bgcolor("white")
    t.pencolor("black")
    t.pensize(3)
    t.speed(0)
    t.setheading(0)

    # left vertical line
    t.hideturtle()
    t.penup()
    t.goto(-150, 0)
    t.pendown()
    t.forward(300)

    # right vertical line
    t.penup()
    t.goto(-150, 100)
    t.pendown()
    t.forward(300)

    # high horizontal line
    t.penup()
    t.goto(-50, -100)
    t.pendown()
    t.setheading(90)
    t.forward(300)

    # low horizontal line
    t.penup()
    t.goto(50, -100)
    t.pendown()
    t.forward(300)
    t.penup()

    # write cell numbers for better user experience
    for cell, coord in frame_line.items():
        t.goto(coord[0] - 40, coord[1] + 30)
        t.write(cell)

# initial draw
tic_tac_toe()


def computer_moves():
    """
    the func creates a list, and enters free spots into it,
    then randomly selects one of them so the computer can play
    """
    available=[]
    for cell in board_status:
        if board_status[cell] == 0:
            available.append(cell)
    move = r.choice(available)
    return move


# to know which spot is taken by whom, if by cross it will be 1, if by circle it will be 2, and if free it will be 0
board_status = {(1, 1): 0, (1, 2): 0, (1, 3): 0,
                (2, 1): 0, (2, 2): 0, (2, 3): 0,
                (3, 1): 0, (3, 2): 0, (3, 3): 0}



def draw_line(start, end):
    """function to draw winning line from the start to end point by frame_line dict"""
    t.penup()
    t.goto(start[0], start[1]) #takes the starting cell from the dict
    t.pendown()
    t.pencolor('red')
    t.goto(end[0], end[1]) #takes the ending cell from the dict
    t.penup()
    t.goto(0,0)



def do_circle(row, col):
    """ function to draw circle"""
    x = -70 + 100 * (col - 1)
    y = 150 - 100 * (row - 1)
    t.goto(x, y)
    t.pendown()
    t.circle(30)
    t.penup()
    board_status[(row, col)] = 2



def do_cross(row, col):
    """function to draw cross"""
    x = -70 + 100 * (col - 1)
    y = 180 - 100 * (row - 1)
    t.goto(x, y)
    t.pendown()
    t.setheading(225)
    t.forward(80)
    t.penup()
    t.goto(x - 60, y)
    t.pendown()
    t.setheading(135)
    t.backward(80)
    t.penup()
    t.setheading(90)
    board_status[(row, col)] = 1

def check_spot(row, col):
    """function to check if the spot is free or taken"""
    if board_status[(row, col)] == 0:
        return True
    else:
        return False


# Winning combinations constant
WINNING_COMBINATIONS = [[(1, 1), (1, 2), (1, 3)],
                        [(2, 1), (2, 2), (2, 3)],
                        [(3, 1), (3, 2), (3, 3)],
                        [(1, 1), (2, 1), (3, 1)],
                        [(1, 2), (2, 2), (3, 2)],
                        [(1, 3), (2, 3), (3, 3)],
                        [(1, 1), (2, 2), (3, 3)],
                        [(1, 3), (2, 2), (3, 1)]]


def check_winner():
    """
    function to check if there is a winner after each move,
    by checking all winning combinations in the board_status dict
    """
    for combination in WINNING_COMBINATIONS:
        values = [board_status[cell] for cell in combination]
        if values == [1, 1, 1]:
            draw_line(frame_line[combination[0]], frame_line[combination[2]])
            t.pencolor("red")
            t.write("Cross wins!", align="center", font=("Arial", 24, "bold"))
            return 1 # Cross wins
        if values == [2, 2, 2]:
            draw_line(frame_line[combination[0]], frame_line[combination[2]])
            t.pencolor("red")
            t.write("Circle wins!", align="center", font=("Arial", 24, "bold"))
            return 2 # Circle wins
    return None # No winner yet


# helper: find best move for 'difficult' level (attack + blocking)
def find_best_move(computer_symbol):
    """
    Return a cell (row,col) for the computer to play.
    Strategy (attack then blocking) - getting information from the combinations and board_status:
    1. If the computer can win in one move (two computer marks + one empty) play that winning cell.
    2. Else, if opponent has two in a winning combination and the third is empty, block it.
    3. Else, if center (2,2) is free, take it.
    4. Else, return a random available cell.
    """
    # map symbol to board_status value
    comp_val = 1 if computer_symbol == 'X' else 2
    opp_val = 2 if comp_val == 1 else 1

    # 1) Try to win: look for a combo with two comp marks and one empty
    for combo in WINNING_COMBINATIONS:
        vals = [board_status[cell] for cell in combo]
        if vals.count(comp_val) == 2 and vals.count(0) == 1:
            for cell in combo:
                if board_status[cell] == 0:
                    return cell

    # 2) Block opponent threat (two opponent marks and one empty)
    for combo in WINNING_COMBINATIONS:
        vals = [board_status[cell] for cell in combo]
        if vals.count(opp_val) == 2 and vals.count(0) == 1:
            for cell in combo:
                if board_status[cell] == 0:
                    return cell

    # 3) No immediate win or block -> take center if free
    if board_status[(2,2)] == 0:
        return (2,2)

    # 4) Take one of the corners if free
    corners = [(1, 1), (1, 3), (3, 1), (3, 3)]
    available_corners = []
    for corner in corners:
        if board_status[corner] == 0:
            available_corners.append(corner)
    if available_corners:
        return r.choice(available_corners)

    # 4) fallback to random available cell
    return computer_moves()


# mapping from symbol to draw function by func address
DRAW_FN = {'X': do_cross, 'O': do_circle}


def append_history(first_player_name, second_player_name, winner_name, filename=HISTORY_FILE):
    """Append a single CSV line: first,second,winner"""
    f = open(filename, 'a', encoding='utf-8')
    f.write(f"player 1: {first_player_name}, player 2: {second_player_name}, player won: {winner_name}\n")
    f.close()


def view_history(filename=HISTORY_FILE):
    """Read history and show it in a dialog."""
    try:
        f = open(filename, 'r', encoding='utf-8')
        # Create an empty list to store the lines
        lines = []
        # Go over each line in the file one by one
        for line in f:
            clean_line = line.strip()  # Remove invisible "Enter" or spaces
            if clean_line != "":  # Only add if the line is not empty
                lines.append(clean_line)

        f.close()
    except Exception:
        t.textinput('History', 'No history available (press OK).')
        return

    if len(lines) == 0: # No history
        t.textinput('History', 'No history available (press OK).')
        return

    lines.reverse() # Flip the list so the newest is at the top

    content = '\n'.join(lines[0:20]) # Take the first 20 from the flipped list
    t.textinput('History (Latest First)', content)


def prompt_cell(p_name):
    """
    Prompt for row and col using turtle numinput and return as ints.
    The user may enter 0 for either prompt to save. Enter 4 to view history. Cancel (None) will exit the program.
    """
    while True:
        # prompt for row; allow 0 to save, 4 to view history
        row_val = t.numinput(f'Input Needed - {p_name}', "Enter row (1-3), 0 to save, or 4 to view history:", minval=0, maxval=4)
        if row_val is None:
            # user cancelled -> close turtle window and exit
            t.bye()
            raise SystemExit
        row = int(row_val)
        if row == 0:
            save_state()
            continue
        if row == 4:
            view_history()
            continue

        # prompt for column; allow 0 to save, 4 to view history
        col_val = t.numinput(f'Input Needed - {p_name}', "Enter column (1-3), 0 to save, or 4 to view history:", minval=0, maxval=4)
        if col_val is None:
            t.bye()
            raise SystemExit
        col = int(col_val)
        if col == 0:
            save_state()
            continue
        if col == 4:
            view_history()
            continue

        return row, col


def get_human_move(current_symbol):
    """Repeatedly prompt the human until they choose an available spot."""
    p_name = "cross" if current_symbol == 'X' else "circle"
    while True:
        row, col = prompt_cell(p_name)
        if check_spot(row, col):
            return row, col
        # inform user and loop
        t.textinput("Error", "This spot is taken, try again! (press OK to continue).")


def choose_computer_move(level, computer_symbol):
    """Return (row,col) for computer move depending on level."""
    if level == '2':
        return find_best_move(computer_symbol)
    return computer_moves()

def save_state(filename=SAVE_FILE):
    """Save board_status, turn, player & computer symbols, and level to a binary file."""
    state = {'board_status': board_status,'turn': turn,'player_symbol': player_symbol,
             'computer_symbol': computer_symbol,'level': level}
    try:
        with open(filename, 'wb') as f:
            p.dump(state, f)
        # confirmation (show filename)
        t.textinput("Saved", f"Game saved to {filename}. Press OK to continue.")
    except Exception as e:
        t.textinput("Save error", f"Failed to save: {e}")


def load_state(filename=SAVE_FILE):
    """Load game state from file and redraw the board. Returns True on success."""
    global board_status, turn, player_symbol, computer_symbol, level # use variable with loaded data
    try:
        with open(filename, 'rb') as f:
            state = p.load(f)
    except Exception as e:
        t.textinput("Load failed", f"No saved game found or load error: {e}. Press OK to continue.")
        return False

    # Safely get the board state and check if it's a valid dictionary
    loaded_board = state.get('board_status')
    if isinstance(loaded_board, dict):
        board_status = loaded_board
    # Update game variables using .get() to provide default values if data is missing
    turn = int(state.get('turn', 0))
    player_symbol = state.get('player_symbol')
    computer_symbol = state.get('computer_symbol')
    level = state.get('level', '1')

    # redraw everything: clear screen and draw grid and marks
    t.clear()
    tic_tac_toe()
    for cell, val in board_status.items():
        if val == 1:
            DRAW_FN['X'](*cell)
        elif val == 2:
            DRAW_FN['O'](*cell)
        t.update() # refresh screen after each draw

    t.textinput("Loaded", f"Game loaded from {filename}. Press OK to continue.")
    return True


# Option to load a saved game before starting
raw_load_choice = t.textinput("Load Game", "Type L to load saved game and resume, or press OK to start a new game.")

# remove spaces and convert to uppercase if it's a valid string
load_choice = raw_load_choice.strip().upper() if isinstance(raw_load_choice, str) else ''
resumed = False
if load_choice == 'L':
    resumed = load_state()

if not resumed:
    # Select Game Mode (1 for Human, 2 for Computer)
    game_mode = t.textinput("Game Mode", "press 1 for 2 players, press 2 to play against computer:")
    if game_mode is None or game_mode.strip() not in ("1", "2"): # Check if input is valid; if not, close the program
        t.textinput("Error", "Invalid game mode. Please restart and choose 1 or 2 (press OK to exit).")
        t.bye()

    turn = 0

    # Setup for Two Players mode
    if game_mode.strip() == "1":
        # Get names for both players; use default names if empty
        name_cross = t.textinput('Player name', 'Enter name for Cross (first player):')
        if name_cross is None:
            t.bye(); raise SystemExit
        name_cross = name_cross.strip() if name_cross.strip() else 'Cross'
        name_circle = t.textinput('Player name', 'Enter name for Circle (second player):')
        if name_circle is None:
            t.bye(); raise SystemExit
        name_circle = name_circle.strip() if name_circle.strip() else 'Circle'
        player_symbol = None
        computer_symbol = None
        level = '1'  # unused in two-player but keep variable for unified calls

    else:
        # Setup for Playing Against Computer
        name_human = t.textinput('Your name', 'Enter your name:')
        if name_human is None:
            t.bye(); raise SystemExit
        name_human = name_human.strip() if name_human.strip() else 'Player'
        name_computer = 'Computer'
        # ask for difficulty first
        level = t.textinput("Level", "Press 1 for easy, 2 for difficult")
        if level is None or level.strip() not in ('1', '2'):
            t.textinput("Error", "Invalid level. Restart and choose 1 or 2 (press OK to exit).")
            t.bye()
        level = level.strip()

        pl_symbol = t.textinput("Decide Symbol", "choose your symbol: X or O").upper()
        if pl_symbol is None:
            t.textinput("Error", "No symbol chosen. Please restart and choose X or O (press OK to exit).")
            t.bye()
        pl_symbol = pl_symbol.strip()
        if pl_symbol not in ("X", "O"):
            t.textinput("Error", "Invalid symbol. You must choose 'X' or 'O'. Press OK to exit.")
            t.bye()

        player_symbol = pl_symbol # Assign symbols to player and computer
        computer_symbol = 'O' if player_symbol == 'X' else 'X'


# unified game loop
winner = None
while turn < 9:
    current_symbol = 'X' if turn % 2 == 0 else 'O'

    # determine if this turn is human's
    is_human_turn = (player_symbol is None) or (current_symbol == player_symbol)

    if is_human_turn:
        r_row, r_col = get_human_move(current_symbol)
        DRAW_FN[current_symbol](r_row, r_col) # send the cell to the draw function (cross or circle)
        turn += 1
    else:
        r_row, r_col = choose_computer_move(level, computer_symbol)
        DRAW_FN[current_symbol](r_row, r_col) # send the cell to the draw function (cross or circle)
        turn += 1


    winner = check_winner()
    # if there's a winner, break the loop
    if winner is not None:
        break

# if no winner and all turns used, it's a tie
if winner is None and turn >= 9:
    t.goto(0, 0)
    t.pencolor("red")
    t.write("It's a tie!", align="center", font=("Arial", 24, "bold"))


# at end of game, record to history file
try:
    # determine first and second player names (first=the X player)
    if player_symbol is None:
        # two-player
        first_player_name = name_cross
        second_player_name = name_circle
    else:
        # vs computer
        if player_symbol == 'X':
            first_player_name = name_human
            second_player_name = name_computer
        else:
            first_player_name = name_computer
            second_player_name = name_human

    if winner is None:
        winner_name = 'Tie'
    elif winner == 1:
        # cross won
        # circle corresponds to first_player_name
        winner_name = first_player_name
    else:
        # circle won
        winner_name = second_player_name
    append_history(first_player_name, second_player_name, winner_name)
except Exception:
    t.goto(0, -200)
    t.pencolor("red")
    t.write("Could not update history file", align="center", font=("Arial", 10, "normal"))


t.done()

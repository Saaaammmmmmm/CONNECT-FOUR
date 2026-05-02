import sys, pygame
import random
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import copy
import sys #for this type of thing I am not giving credit to any ai or google search because I specifically looked up, for example, how to increase the loop limit when I got an error.




#VARIABLES====================================
#graphics-related
H_CELLS = 7
V_CELLS = 6
CELL_SIZE = 72
HALF_C = CELL_SIZE/2
H_LEN = H_CELLS*CELL_SIZE
V_LEN = V_CELLS*CELL_SIZE
BLUE_GRID = "#0270ad"
Y_PEICE = "#ffe02e"
R_PEICE = "#f0422d"
OFF_WHITE ="#fafafa"
OFF_WHITE_2 ="#caeded"
LIGHT_GREEN = "#6a8c5f"
OTHER_GREEN = "#3c6352"
BUTTON_YELLOW = "#f7ee3b"
BUTTON_RED = "#d66974"
clock = pygame.time.Clock()


clicked_col_choice = 0
restart = True
menu_up = True
red_thinking = False
stop = False
first_turn = True

#logic-related
board = [["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "", "  ", "  ", "  ", "  "]] 
whose_turn = "N/A" 
yellow_wins = 0
red_wins = 0
number_ties = 0
player_choice = "N/A"
game_over = False
current_winner = "N/A"
tie = False
full_col = False
final_row = -1
computer_choice = -1
R = "🔴 "
Y = "🟡 "
one_player = False
COMP_SKILL = 2
DECAY_RATE = 0.6
WIN_MULTIPLIER = 6
LOSE_MULTIPLIER = 7
THREE_ROW_MULTIPLIER = 4
TWO_ROW_MULTIPLIER = 2


#PYGAME INITIALISATION STUFF==================
pygame.init()
size = width, height = H_LEN+CELL_SIZE, V_LEN+2*CELL_SIZE
screen = pygame.display.set_mode(size)
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 4*CELL_SIZE // 5)
small_font = pygame.font.Font(pygame.font.get_default_font(), 2*CELL_SIZE // 5)
mini_font = pygame.font.Font(pygame.font.get_default_font(), 2*CELL_SIZE // 9)
big_font = pygame.font.Font(pygame.font.get_default_font(), 8*CELL_SIZE // 5)
sys.setrecursionlimit(7**(2*COMP_SKILL)+1)

#=============FUNCTIONS===============





#Print Board





#Take Turn (Get input for where the player wants to go)
def take_turn():
    global player_choice, board, computer_choice
    if one_player == True and whose_turn == "red":
        computer_choice = calculate_computer_choice(board) + 1
        drop_peice("red", board, computer_choice)
        return
    ask_for_player_to_pick = whose_turn +" pick: "
    player_choice = clicked_col_choice

    if player_choice == "1" or player_choice == "2" or player_choice == "3" or player_choice == "4" or  player_choice =="5" or player_choice == "6" or player_choice == "7":
        player_choice = int(player_choice)
        drop_peice(whose_turn, board, player_choice)
    elif player_choice == "restart" or player_choice == "reset" or player_choice == "clear":
        restart()
        take_turn()
    else:
        print("Sorry, I don't understand", player_choice)
        take_turn()




#Count the amount of 3 in a rows with places for 4 in a row
def count_3_in_a_row(board, row, col, piece):
    total_count = 0
    # Horizontal
    horizontal_peice_count = 0
    horizontal_space_count = 0
   
    for i in range(max(0, col - 3), min(7, col + 4)): #Max/min function from github copilot AI
        if board[row][i] == piece:
            horizontal_peice_count += 1
        elif board[row][i] == "  ":
            horizontal_space_count += 1
        else:
            horizontal_peice_count = 0
            horizontal_space_count = 0




        if horizontal_peice_count == 3 and horizontal_space_count == 1:
            total_count += 1
            horizontal_peice_count = 0
            horizontal_space_count = 0
   
    # Vertical
    vertical_peice_count = 0
    vertical_space_count = 0
    for i in range(max(0, row - 3), min(6, row + 4)):
        if board[i][col] == piece:
            vertical_peice_count += 1
        elif board[i][col] == "  ":
            vertical_space_count += 1
        else:  
            vertical_peice_count = 0
            vertical_space_count = 0




        if vertical_peice_count == 3 and vertical_space_count == 1:
            total_count += 1
            vertical_peice_count = 0
            vertical_space_count = 0
   
    # Diagonal /
    positive_diagonal_peice_count = 0
    positive_diagonal_space_count = 0
    for i in range(-3, 4):
        r = row + i
        c = col + i
        if 0 <= r < 6 and 0 <= c < 7:
            if board[r][c] == piece:
                positive_diagonal_peice_count += 1
            elif board[r][c] == "  ":
                positive_diagonal_space_count += 1
            else:
                positive_diagonal_peice_count = 0
                positive_diagonal_space_count = 0
           
            if positive_diagonal_peice_count == 3 and positive_diagonal_space_count == 1:
                total_count += 1
                positive_diagonal_peice_count = 0
                positive_diagonal_space_count = 0
   
    # Diagonal \
    negative_diagonal_peice_count = 0
    negative_diagonal_space_count = 0
    for i in range(-3, 4):
        r = row - i
        c = col + i
        if 0 <= r < 6 and 0 <= c < 7:
            if board[r][c] == piece:
                negative_diagonal_peice_count += 1
            elif board[r][c] == "  ":
                negative_diagonal_space_count += 1
            else:
                negative_diagonal_peice_count = 0
                negative_diagonal_space_count = 0
           
            if negative_diagonal_peice_count == 3 and negative_diagonal_space_count == 1:
                total_count += 1
                negative_diagonal_peice_count = 0
                negative_diagonal_space_count = 0
   
    return total_count




#Count the amount of 2 in a rows with places for 4 in a row
def count_2_in_a_row(board, row, col, piece):
    total_count = 0
    # Horizontal
    horizontal_peice_count = 0
    horizontal_space_count = 0
   
    for i in range(max(0, col - 3), min(7, col + 4)): #Max/min function from github copilot AI
        if board[row][i] == piece:
            horizontal_peice_count += 1
        elif board[row][i] == "  ":
            horizontal_space_count += 1
        else:
            horizontal_peice_count = 0
            horizontal_space_count = 0




        if horizontal_peice_count == 2 and horizontal_space_count == 2:
            total_count += 1
            horizontal_peice_count = 0
            horizontal_space_count = 0
   
    # Vertical
    vertical_peice_count = 0
    vertical_space_count = 0
    for i in range(max(0, row - 3), min(6, row + 4)):
        if board[i][col] == piece:
            vertical_peice_count += 1
        elif board[i][col] == "  ":
            vertical_space_count += 1
        else:  
            vertical_peice_count = 0
            vertical_space_count = 0




        if vertical_peice_count == 2 and vertical_space_count == 2:
            total_count += 1
            vertical_peice_count = 0
            vertical_space_count = 0
   
    # Diagonal /
    positive_diagonal_peice_count = 0
    positive_diagonal_space_count = 0
    for i in range(-3, 4):
        r = row + i
        c = col + i
        if 0 <= r < 6 and 0 <= c < 7:
            if board[r][c] == piece:
                positive_diagonal_peice_count += 1
            elif board[r][c] == "  ":
                positive_diagonal_space_count += 1
            else:
                positive_diagonal_peice_count = 0
                positive_diagonal_space_count = 0
           
            if positive_diagonal_peice_count == 2 and positive_diagonal_space_count == 2:
                total_count += 1
                positive_diagonal_peice_count = 0
                positive_diagonal_space_count = 0
   
    # Diagonal \
    negative_diagonal_peice_count = 0
    negative_diagonal_space_count = 0
    for i in range(-3, 4):
        r = row - i
        c = col + i
        if 0 <= r < 6 and 0 <= c < 7:
            if board[r][c] == piece:
                negative_diagonal_peice_count += 1
            elif board[r][c] == "  ":
                negative_diagonal_space_count += 1
            else:
                negative_diagonal_peice_count = 0
                negative_diagonal_space_count = 0
           
            if negative_diagonal_peice_count == 2 and negative_diagonal_space_count == 2:
                total_count += 1
                negative_diagonal_peice_count = 0
                negative_diagonal_space_count = 0
   
    return total_count




#Computer Turn Simulated
def computer_turn(board, col, pick, c, n):
    drop_peice("red", board, col+1)
    if not full_col:
        if calc_win(board):
            pick[c] += WIN_MULTIPLIER*(DECAY_RATE ** n)
            return
        elif calc_tie(board):
            return
       


        pick[c] += (DECAY_RATE ** n) * THREE_ROW_MULTIPLIER * count_3_in_a_row(board, final_row, col, R)
        pick[c] += (DECAY_RATE ** n) * TWO_ROW_MULTIPLIER * count_2_in_a_row(board, final_row, col, R)


       
        #continue to evaluate next turn
        new_board = copy.deepcopy(board)
        n2 = n
        for column in range(7):
            n = n2
            board = copy.deepcopy(new_board)
            player_turn(board, column, pick, c, n)




#Player Turn Simulated
def player_turn(board, col, pick, c, n):
    drop_peice("yellow", board, col+1)
    if not full_col:
        n -= 1
        if calc_loss(board):
            pick[c] -= LOSE_MULTIPLIER*(DECAY_RATE ** (n + 1))
        elif calc_tie(board):
            return
       
        pick[c] -= (DECAY_RATE ** n) * THREE_ROW_MULTIPLIER * count_3_in_a_row(board, final_row, col, Y)
        pick[c] -= (DECAY_RATE ** n) * TWO_ROW_MULTIPLIER * count_2_in_a_row(board, final_row, col, Y)


       
        #continue to evaluate next turn
        if n != 0:
            new_board = copy.deepcopy(board)
            n2 = n
            for column in range(7):
                n = n2
                board = copy.deepcopy(new_board)
                computer_turn(board, column, pick, c, n)




#Calculate Computer Choice
def calculate_computer_choice(a_board):
    global red_thinking
    og_board = copy.deepcopy(a_board)
    board = copy.deepcopy(a_board)
   
    #Check for an immediate win
    for col in range(7):
        board = copy.deepcopy(a_board)
        drop_peice("red", board, col+1)
        if calc_win(board):
            return col
   
    #Check for blocking an immediate loss
    for col in range(7):
        board = copy.deepcopy(a_board)
        drop_peice("yellow", board, col+1)
        if calc_loss(board):
            return col
   

    red_thinking = True 
   
    #Otherwise, simulate future moves and give them a rating
    pick = [0, 0, 0, 0, 0, 0, 0, -99999999999]
    n = COMP_SKILL
    n2 = n
    for col in range(7):
        n = n2
        board = copy.deepcopy(a_board)
        computer_turn(board, col, pick, col, n)
   
    evaluation_order = [3,4,2,5,1,6,0] #if there is a tie, picks middlemost column
    best_choice = 7
    redo = True
    while redo:
        for option in evaluation_order:
            redo = False
            if pick[option] > pick[best_choice]:
                best_choice = option
            drop_peice("red", board, option+1)
            board = copy.deepcopy(a_board)
            if full_col:
                evaluation_order.remove(option)
                best_choice = evaluation_order[0]
                redo = True
                break
           
   
    a_board = copy.deepcopy(og_board)
    red_thinking = False
    return best_choice




#Update board
def drop_peice(wt, board, choice):
    global full_col, final_row
    choice = choice - 1
    peice = "N/A"
    full_col = False
    if wt == "red":
        peice = R
    else:
        peice = Y
   
    final_row = -1
    for i in range(6):
        row = 5-i
        if board[row][choice] == "  ":
            board[row][choice] = peice
            final_row = row
            return
       
    #if the loop finds no empty spots
    full_col = True




#transition turn
def transition_turn(wt):
    global whose_turn, player_choice
    if wt == "red":
        whose_turn = "yellow"
    else:
        whose_turn = "red"




#Is the game over
def end_game():
    global game_over, red_wins, yellow_wins, current_winner, tie, number_ties
    #Check for horizontal wins
    r_count = 0
    y_count = 0
    for row in range(6):
        r_count = 0
        y_count = 0
        for i in range(7):
            if board[row][i] == Y: #counts the amount of peices of the same color in a row
                y_count = y_count + 1
                r_count = 0
            elif board[row][i] == R:
                r_count = r_count + 1
                y_count = 0
            else:
                r_count = 0
                y_count = 0
               
            #determines if there were 4 in a row
            if r_count == 4:
                game_over = True
                red_wins = red_wins + 1
                current_winner = "Red"
                return
            elif y_count == 4:
                game_over = True
                yellow_wins = yellow_wins + 1
                current_winner = "Yellow"
                return
       
   
    #Check for vertical wins
    r_count = 0
    y_count = 0
   
    for column in range(7):
        r_count = 0
        y_count = 0
       
        for i in range(6):
            if board[i][column] == Y: #counts the amount of peices of the same color in a row
                y_count = y_count + 1
                r_count = 0
            elif board[i][column] == R:
                r_count = r_count + 1
                y_count = 0
            else:
                r_count = 0
                y_count = 0
               
            #determines if there were 4 in a row
            if r_count == 4:
                game_over = True
                red_wins = red_wins + 1
                current_winner = "Red"
                return
            elif y_count == 4:
                game_over = True
                yellow_wins = yellow_wins + 1
                current_winner = "Yellow"
                return
       
    #Check for diagonal wins
    #negative Diagonal wins (like positive growth on a graph)
    for row in range(3):
        for column in range(4):
            if board[row][column] == board[row+1][column+1] == board[row+2][column+2] == board[row+3][column+3]:
                if board[row][column] == R:
                    game_over = True
                    red_wins = red_wins + 1
                    current_winner = "Red"
                elif board[row][column] == Y:
                    game_over = True
                    yellow_wins = yellow_wins + 1
                    current_winner = "Yellow"
    #for positive diagonals
    for row in range(3, 6):
        for column in range(4):
            if board[row][column] == board[row-1][column+1] == board[row-2][column+2] == board[row-3][column+3]:
                if board[row][column] == R:
                    game_over = True
                    red_wins = red_wins + 1
                    current_winner = "Red"
                elif board[row][column] == Y:
                    game_over = True
                    yellow_wins = yellow_wins + 1
                    current_winner = "Yellow"




    #Check for tie
    for row in range(6):
        for column in range(7):
            if board[row][column] == "  ":
                return
    #Will only happen if there are no blank spaces:
    tie = True
    game_over = True
    current_winner = "tie"
    number_ties +=1




#Would I win?
def calc_win(board): # just does true or false, should go faster than end_game
    #Check for horizontal wins
    for row in range(6):
        r_count = 0
        for i in range(7):
            if board[row][i] == R:
                r_count = r_count + 1
            else:
                r_count = 0
               
            #determines if there were 4 in a row
            if r_count == 4:
                return True
   
    #Check for vertical wins
    for column in range(7):
        r_count = 0
       
        for i in range(6):
            if board[i][column] == R:
                r_count = r_count + 1
            else:
                r_count = 0
               
            #determines if there were 4 in a row
            if r_count == 4:
                return True
       
    #Check for diagonal wins
    #negative Diagonal wins (like positive growth on a graph)
    for row in range(3):
        for column in range(4):
            if board[row][column] == board[row+1][column+1] == board[row+2][column+2] == board[row+3][column+3]:
                if board[row][column] == R:
                    return True
    #for positive diagonals
    for row in range(3, 6):
        for column in range(4):
            if board[row][column] == board[row-1][column+1] == board[row-2][column+2] == board[row-3][column+3]:
                if board[row][column] == R:
                    return True




#Would I lose?
def calc_loss(board): # just does true or false, should go faster than end_game
    #Check for horizontal wins
    for row in range(6):
        y_count = 0
        for i in range(7):
            if board[row][i] == Y:
                y_count = y_count + 1
            else:
                y_count = 0
               
            #determines if there were 4 in a row
            if y_count == 4:
                return True
   
    #Check for vertical wins
    for column in range(7):
        y_count = 0
       
        for i in range(6):
            if board[i][column] == Y:
                y_count = y_count + 1
            else:
                y_count = 0
               
            #determines if there were 4 in a row
            if y_count == 4:
                return True
       
    #Check for diagonal wins
    #negative Diagonal wins (like positive growth on a graph)
    for row in range(3):
        for column in range(4):
            if board[row][column] == board[row+1][column+1] == board[row+2][column+2] == board[row+3][column+3]:
                if board[row][column] == Y:
                    return True
    #for positive diagonals
    for row in range(3, 6):
        for column in range(4):
            if board[row][column] == board[row-1][column+1] == board[row-2][column+2] == board[row-3][column+3]:
                if board[row][column] == Y:
                    return True




#Is there a tie?
def calc_tie(board):
    #Check for tie
    for row in range(6):
        for column in range(7):
            if board[row][column] == "  ":
                return
    #Will only happen if there are no blank spaces:
    return True




#Reset Game
def reset(): #resets and checks if it is at the end of the game, not mid-match
    global board, whose_turn, game_over, tie, current_winner
    if game_over == True:
        board = [["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "], ["  ", "  ", "  ", "  ", "  ", "  ", "  "]]
        turn_picker = random.randint(1,2)
        if turn_picker == 1:
            whose_turn = "red"
        else:
            whose_turn = "yellow"
        game_over = False
        tie = False
        current_winner = "N/A"
        




#Restart Mid-match
def restart():
    global yellow_wins, red_wins, number_ties, game_over
    yellow_wins = 0
    red_wins = 0
    number_ties = 0
    game_over = True
    reset()
           

#-------------EVENT LOOP----------------
while 1:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Game interaction
            if (pygame.mouse.get_pos()[0] >= HALF_C) and (pygame.mouse.get_pos()[0] - HALF_C) <= H_LEN and (pygame.mouse.get_pos()[1] >= HALF_C) and (pygame.mouse.get_pos()[1] - HALF_C) <= V_LEN and not menu_up and not stop and not (whose_turn == "red" and one_player == True):
                column = int(pygame.mouse.get_pos()[0]-HALF_C) // CELL_SIZE
                clicked_col_choice = str(column + 1)
                if not ( one_player and whose_turn == "red" and not game_over and not menu_up):
                    take_turn()
                end_game()
                if game_over:
                    stop = True
                elif not stop:
                    reset()
                    transition_turn(whose_turn)
            #Menu Buttons 
            if menu_up:
                if (size[0]/2 + HALF_C - 2.7*CELL_SIZE < pygame.mouse.get_pos()[0] < size[0]/2 + HALF_C - 2.7*CELL_SIZE + 2.1*CELL_SIZE and size[1]/2 + HALF_C - .75*CELL_SIZE < pygame.mouse.get_pos()[1] < size[1]/2 + HALF_C - .75*CELL_SIZE + 1.5*CELL_SIZE): #These statements are also from anthropic claude sonnet (just the dimentions), because I know how but do not have time to write them
                    game_over = True
                    reset()
                    one_player = True
                    menu_up = False
                    turn_picker = random.randint(1,2)
                    if turn_picker == 1:
                        whose_turn = "red"
                    else:
                        whose_turn = "yellow"
                    first_turn = False
                elif (size[0]/2 + HALF_C - .4*CELL_SIZE < pygame.mouse.get_pos()[0] < size[0]/2 + HALF_C - .4*CELL_SIZE + 2.1*CELL_SIZE and size[1]/2 + HALF_C - .75*CELL_SIZE < pygame.mouse.get_pos()[1] < size[1]/2 + HALF_C - .75*CELL_SIZE + 1.5*CELL_SIZE):
                    game_over = True
                    reset()
                    one_player = False
                    menu_up = False
                    first_turn = False
                if not first_turn:    
                    if (size[0]/2 + HALF_C - 2.7*CELL_SIZE < pygame.mouse.get_pos()[0] < size[0]/2 + HALF_C - 2.7*CELL_SIZE + 2.1*CELL_SIZE and size[1]/2 + HALF_C + .85*CELL_SIZE < pygame.mouse.get_pos()[1] < size[1]/2 + HALF_C + .85*CELL_SIZE + .65*CELL_SIZE):
                        restart()
                        menu_up = False
                    elif (size[0]/2 + HALF_C - .4*CELL_SIZE < pygame.mouse.get_pos()[0] < size[0]/2 + HALF_C - .4*CELL_SIZE + 2.1*CELL_SIZE and size[1]/2 + HALF_C + .85*CELL_SIZE < pygame.mouse.get_pos()[1] < size[1]/2 + HALF_C + .85*CELL_SIZE + .65*CELL_SIZE):
                        menu_up = False
            
            else: #MENU IS DOWN
                if (size[0] - CELL_SIZE - CELL_SIZE*1.5 < pygame.mouse.get_pos()[0] < size[0] - CELL_SIZE and size[1] - 4*CELL_SIZE//7 < pygame.mouse.get_pos()[1] < size[1] - 4*CELL_SIZE//7 + CELL_SIZE//2):
                    menu_up = True
                elif (CELL_SIZE < pygame.mouse.get_pos()[0] < CELL_SIZE + CELL_SIZE*1.5 and size[1] - 4*CELL_SIZE//7 < pygame.mouse.get_pos()[1] < size[1] - 4*CELL_SIZE//7 + CELL_SIZE//2):
                    stop = False
                    game_over = True
                    reset()
    
    
    
    
    
    
    
    
    #DRAW STUFF ____________
    
    #BACKGROUND
    screen.fill(OFF_WHITE)
    
    #DRAW BOARD
    #Draw outline
    pygame.draw.rect(screen, BLUE_GRID, (4/5*HALF_C, 4/5*HALF_C, H_LEN + 1/5*CELL_SIZE, V_LEN+ 1/5*CELL_SIZE))
    #Draw stilts
    pygame.draw.rect(screen, BLUE_GRID, (4/5*HALF_C, 4/5*HALF_C + V_LEN+ 1/5*CELL_SIZE-1, HALF_C, CELL_SIZE))
    pygame.draw.rect(screen, BLUE_GRID, (H_LEN+1/5*HALF_C-1, V_LEN + HALF_C, HALF_C, CELL_SIZE))
    #Punch Holes
    for h in range(H_CELLS):
        for v in range(V_CELLS):
            pygame.draw.circle(screen, OFF_WHITE, (CELL_SIZE + CELL_SIZE*h, CELL_SIZE + CELL_SIZE*v), 4/5*HALF_C)
    
    #Draw Peices
    for col in range(7):
        for row in range(6):
            if board[row][col] == R:
                pygame.draw.circle(screen, R_PEICE, (CELL_SIZE + CELL_SIZE*col, CELL_SIZE + CELL_SIZE*row), 4/5*HALF_C)
            elif board[row][col] == Y:
                pygame.draw.circle(screen, Y_PEICE, (CELL_SIZE + CELL_SIZE*col, CELL_SIZE + CELL_SIZE*row), 4/5*HALF_C)
    
    

    
#Draw Start Menu
    if menu_up:
        #RECTANGLE AND BOARDER
        pygame.draw.rect(screen, LIGHT_GREEN, (size[0]/2 -2.5*CELL_SIZE, size[1]/2-2.25*CELL_SIZE,  5*CELL_SIZE, 4.5*CELL_SIZE))
        pygame.draw.rect(screen, OTHER_GREEN, (size[0]/2 -2.5*CELL_SIZE, size[1]/2-2.25*CELL_SIZE,  5*CELL_SIZE, 4.5*CELL_SIZE), CELL_SIZE//6)
        pygame.draw.rect(screen, OTHER_GREEN, (size[0]/2 -2.5*CELL_SIZE, size[1]/2-2.25*CELL_SIZE,  5*CELL_SIZE, 4.5*CELL_SIZE), CELL_SIZE//6)
        #"CONNECT FOUR" TEXT
        title_render = font.render("CONNECT", True, OFF_WHITE_2)
        title_rect = title_render.get_rect( center = (size[0]/2, size[1]/2 - 1.6*CELL_SIZE) )
        title_render2 = font.render("FOUR", True, OFF_WHITE_2)
        title_rect2 = title_render2.get_rect( center = (size[0]/2, size[1]/2 - .8*CELL_SIZE) )
        screen.blit(title_render, title_rect)
        screen.blit(title_render2, title_rect2)
        
        #LEFT TOP BUTTON (One Player)
        pygame.draw.rect(screen, BUTTON_YELLOW, (size[0]/2 + HALF_C - 2.7*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE,  2.1*CELL_SIZE, 1.5*CELL_SIZE))
        pygame.draw.rect(screen, BUTTON_RED, (size[0]/2 + HALF_C - 2.7*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE,  2.1*CELL_SIZE, 1.5*CELL_SIZE), CELL_SIZE // 10)
        #text 
        oneplayer_render = small_font.render("One", True, "grey43")
        oneplayer_rect = oneplayer_render.get_rect( center = (size[0]/2 + HALF_C - 2.7*CELL_SIZE + 1.05*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE + .55*CELL_SIZE) )
        oneplayer_render2 = small_font.render("Player", True, "grey43")
        oneplayer_rect2 = oneplayer_render2.get_rect( center = (size[0]/2 + HALF_C - 2.7*CELL_SIZE + 1.05*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE + .95*CELL_SIZE) )
        screen.blit(oneplayer_render, oneplayer_rect)
        screen.blit(oneplayer_render2, oneplayer_rect2)
        
        #RIGHT TOP BUTTON (Two Player)
        pygame.draw.rect(screen, BUTTON_YELLOW, (size[0]/2 + HALF_C - .4*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE,  2.1*CELL_SIZE, 1.5*CELL_SIZE))
        pygame.draw.rect(screen, BUTTON_RED, (size[0]/2 + HALF_C - .4*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE,  2.1*CELL_SIZE, 1.5*CELL_SIZE), CELL_SIZE // 10)
        #text #Written by Anthropic Claude Sonnet 4.5 (because I know how but do not have time to)
        twoplayer_render = small_font.render("Two", True, "grey43")
        twoplayer_rect = twoplayer_render.get_rect( center = (size[0]/2 + HALF_C - .4*CELL_SIZE + 1.05*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE + .55*CELL_SIZE) )
        twoplayer_render2 = small_font.render("Player", True, "grey43")
        twoplayer_rect2 = twoplayer_render2.get_rect( center = (size[0]/2 + HALF_C - .4*CELL_SIZE + 1.05*CELL_SIZE, size[1]/2 + HALF_C - .75*CELL_SIZE + .95*CELL_SIZE) )
        screen.blit(twoplayer_render, twoplayer_rect)
        screen.blit(twoplayer_render2, twoplayer_rect2)
        if not first_turn:
            #LEFT BOTTOM BUTTON (Clear Score Count)
            pygame.draw.rect(screen, BUTTON_RED, (size[0]/2 + HALF_C - 2.7*CELL_SIZE, size[1]/2 + HALF_C + .85*CELL_SIZE,  2.1*CELL_SIZE, .65*CELL_SIZE))
            pygame.draw.rect(screen, BUTTON_YELLOW, (size[0]/2 + HALF_C - 2.7*CELL_SIZE, size[1]/2 + HALF_C + .85*CELL_SIZE,  2.1*CELL_SIZE, .65*CELL_SIZE), CELL_SIZE//18)
            #text #Written by Anthropic Claude Sonnet 4.5 (because I know how but do not have time to)
            clearscore_render = mini_font.render("Clear Score Count", True, OFF_WHITE_2)
            clearscore_rect = clearscore_render.get_rect( center = (size[0]/2 + HALF_C - 2.7*CELL_SIZE + 1.05*CELL_SIZE, size[1]/2 + HALF_C + .85*CELL_SIZE + .325*CELL_SIZE) )
            screen.blit(clearscore_render, clearscore_rect)
            
            #RIGHT BOTTOM BUTTON (Exit)
            pygame.draw.rect(screen, BUTTON_RED, (size[0]/2 + HALF_C - .4*CELL_SIZE, size[1]/2 + HALF_C + .85*CELL_SIZE,  2.1*CELL_SIZE, .65*CELL_SIZE))
            pygame.draw.rect(screen, BUTTON_YELLOW, (size[0]/2 + HALF_C - .4*CELL_SIZE, size[1]/2 + HALF_C + .85*CELL_SIZE,  2.1*CELL_SIZE, .65*CELL_SIZE), CELL_SIZE // 18)
            #text #Written by Anthropic Claude Sonnet 4.5 (because I know how but do not have time to)
            exit_render = mini_font.render("Exit", True, OFF_WHITE_2)
            exit_rect = exit_render.get_rect( center = (size[0]/2 + HALF_C - .4*CELL_SIZE + 1.05*CELL_SIZE, size[1]/2 + HALF_C + .85*CELL_SIZE + .325*CELL_SIZE) )
            screen.blit(exit_render, exit_rect)
        
    #Print Whose turn
    if menu_up:
        message = ""
        color = BLUE_GRID
    elif game_over:
        if tie:
            message = "Tie Game!!!"
            color = BLUE_GRID
        else:
            message = current_winner + " Wins!!!"
            if current_winner == "Yellow":
                color = Y_PEICE
            else:
                color = R_PEICE
    elif not one_player:
        
        message = whose_turn + " turn"
        if whose_turn == "N/A":
            message = "click to move"
        elif whose_turn == "yellow":
            color = Y_PEICE
        else:
            color = R_PEICE
    else:
        if whose_turn == "yellow":
            message = "your turn"
            color = Y_PEICE
        else:
            message = "I'm thinking..."
            color = R_PEICE
            
    wt_render = font.render(message, True, color)
    wt_rect = wt_render.get_rect( center = (size[0]/2, size[1] - 1*CELL_SIZE) )
    screen.blit(wt_render, wt_rect)
    #Print Reset Button
    if not menu_up:
        pygame.draw.rect(screen, BUTTON_YELLOW, (CELL_SIZE, size[1] - 4*CELL_SIZE//7, CELL_SIZE*1.5, CELL_SIZE//2))
        pygame.draw.rect(screen, BUTTON_RED, (CELL_SIZE, size[1] - 4*CELL_SIZE//7, CELL_SIZE*1.5, CELL_SIZE//2), CELL_SIZE//20)
        #text
        reset_render = mini_font.render("Reset", True, "grey43")
        reset_rect = reset_render.get_rect(center = (CELL_SIZE + CELL_SIZE*0.75, size[1] - 4*CELL_SIZE//7 + CELL_SIZE//4))
        screen.blit(reset_render, reset_rect)

        # Reset button (left)
        pygame.draw.rect(screen, BUTTON_YELLOW, (CELL_SIZE, size[1] - 4*CELL_SIZE//7, CELL_SIZE*1.5, CELL_SIZE//2))
        pygame.draw.rect(screen, BUTTON_RED, (CELL_SIZE, size[1] - 4*CELL_SIZE//7, CELL_SIZE*1.5, CELL_SIZE//2), CELL_SIZE//20)
        #text
        reset_render = mini_font.render("Reset", True, "grey43")
        reset_rect = reset_render.get_rect(center = (CELL_SIZE + CELL_SIZE*0.75, size[1] - 4*CELL_SIZE//7 + CELL_SIZE//4))
        screen.blit(reset_render, reset_rect)
     #Print Menu Button
        # Menu button (right)
        pygame.draw.rect(screen, BUTTON_YELLOW, (size[0] - CELL_SIZE - CELL_SIZE*1.5, size[1] - 4*CELL_SIZE//7, CELL_SIZE*1.5, CELL_SIZE//2))
        pygame.draw.rect(screen, BUTTON_RED, (size[0] - CELL_SIZE - CELL_SIZE*1.5, size[1] - 4*CELL_SIZE//7, CELL_SIZE*1.5, CELL_SIZE//2), CELL_SIZE//20)
        #text
        menu_render = mini_font.render("Menu", True, "grey43")
        menu_rect = menu_render.get_rect(center = (size[0] - CELL_SIZE - CELL_SIZE*0.75, size[1] - 4*CELL_SIZE//7 + CELL_SIZE//4))
        screen.blit(menu_render, menu_rect)
        
        #print Scores and ties:
        scores_render = mini_font.render("Yellow: " + str(yellow_wins)+ "    Red: " +str(red_wins) + "    Tie: " + str(number_ties), True, BLUE_GRID)
        scores_rect = scores_render.get_rect(center = (size[0]/2, size[1] - 4*CELL_SIZE//7 + CELL_SIZE//4))
        screen.blit(scores_render, scores_rect)
        
    
   
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#Always Last
    pygame.display.flip()
    
    #so the screen updates before the long calculation delay
    if one_player and whose_turn == "red" and not game_over and not menu_up and not stop:
        take_turn()
        end_game()
        if game_over:
            stop = True
        else:
            transition_turn(whose_turn)
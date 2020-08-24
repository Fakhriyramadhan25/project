from IPython.display import clear_output
def display_board(board):
    print(board[7]+'|'+board[8]+'|'+board[9])
    print(board[4]+'|'+board[5]+'|'+board[6])
    print(board[1]+'|'+board[2]+'|'+board[3])

    test_board = ['#','X','O','X','O','X','O','X','X','X']

    display_board(test_board)

#    def player_input():
#    marker = ' '
#    while marker != 'X' and marker != 'O':
#        if marker != 'X' and marker != 'O':
#            print('invalid input')
#        marker = input("Please input whether it's 'X or O': ")
#
#    player1 = marker
#    #Keep asking player 1 to choose
#    if player1 == 'X' :
#        player2= 'O'
#    else:
#        player2 = 'X'
#    return(player1,player2)

    def player2():
    marker = ' '
    while not marker == 'X' and marker == 'O':
        marker = input("Please input whether it's 'X or O': ").upper()
        if not marker == 'X' and marker == 'O':
            print('invalid input')

    if marker == 'X':
        return ('X','O')
    else:
        return ('O','X')

    def place_maker(board, marker,position):
    board[position] = marker

    place_maker(test_board, 'G', 2)
    display_board(test_board)

    def win_check(board, mark):
    #win tic tac toe

    #all rows
    return ((board[1] == mark and board[2] == mark and board[3] == mark ) or
    (board[4] == mark and board[5] == mark and board[6] == mark ) or
    (board[7] == mark and board[8] == mark and board[9] == mark ) or

    #all column
    (board[1] == mark and board[4] == mark and board[7] == mark ) or
    (board[2] == mark and board[5] == mark and board[8] == mark ) or
    (board[3] == mark and board[6] == mark and board[9] == mark ) or

    #2 diagonals
    (board[1] == mark and board[5] == mark and board[9] == mark ) or
    (board[3] == mark and board[5] == mark and board[7] == mark ))

    display_board(testboard)
    win_check(testboard,'x')

    import random
    def choose_first():
    flip = random.randint(0,1)
    if flip == 1:
        return 'Player 1'
    else :
        return 'Player 2'

    def space_check(board, position):
    board[position] == ' '


    import random
    def choose_first():
        flip = random.randint(0,1)
        if flip == 1:
            return 'Player 1'
        else :
            return 'Player 2'


    def space_check(board, position):
    return board[position] == ' '

    def full_board_check(board):
    for i in range(0,10):
        if space_check(board,i):
            return False

    #board is full
    return True

def player_choice(board):

    position = 0

    while pos not in [1,2,3,4,5,6,7,8,9] or not space_check(board,position):
        position = int(input('Choose a position: (1-9)'))
    return position


    def replay():
    input("play again? Enter Yes or No")

    return choice == 'yes'

#while loop to keep running the game
print('Welcome to Tic Tac Toe')

while True:

    #Play the game

    ## set everything up (board, whos first, choose markers X,O)
    the_board = [' ']*10
    player1_maker, player2_maker = player_input()

    turn = choose_first()
    print(turn  + ' will go first')
    play_game = input('ready to play? y or n?')
    if play_game == 'y':
        game_on==True
    else:
        game_on==False

    while game_on:
        if turn == 'Player 1':
            #show the board
            display_board(the_board)
            #choose position
            position = player_choice(the_board)
            # place the marker on the position
            place_marker(the_board,player1_marker, position)
            #check if the won
            if wincheck(the_board, player1_marker):
                display_board(the_board)
                print('Player 1 Has won')
                game_on = False
            else:
                if full_board_check(the_board):
                    display_board(the_baord)
                    print('The game is tie')
                    break
                else:
                    turn = 'Player 2'

        else:
            #show the board
            display_board(the_board)
            #choose position
            position = player_choice(the_board)
            # place the marker on the position
            place_marker(the_board,player2_marker, position)
            #check if the won
            if wincheck(the_board, player2_marker):
                display_board(the_board)
                print('Player 2 Has won')
                game_on = False
            else:
                if full_board_check(the_board):
                    display_board(the_baord)
                    print('The game is tie')
                    break
                else:
                    turn = 'Player 1'
            ## player two turn

    if not replay():
        break
# break out of the while loop on replay

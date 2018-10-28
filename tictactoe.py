#!/usr/bin/python3
import sys

board = [[" " for x in range(3)] for y in range(3)]

def print_board():
    print()
    for i in range(3):
        if i > 0:
            print("---+---+---")
        line = ""
        for j in range(3):
            line = line + " "
            if j > 0:
                line = line + "| "
            line = line + board[i][j]
        print(line)


def check_2(who):
    # rows
    for i in range(3):
        n = 0
        m = 0
        for j in range(3):
            if board[i][j] == who:
                n = n + 1
            elif board[i][j] == " ":
                m = m + 1
        if n==2 and m==1:
            return("R"+str(i))

    # columns
    for j in range(3):
        n = 0
        m = 0
        for i in range(3):
            if board[i][j] == who:
                n = n + 1
            elif board[i][j] == " ":
                m = m + 1
        if n==2 and m==1:
            return("C"+str(j))

    n = 0
    m = 0
    for i in range(3):
        if board[i][i] == who:
            n = n + 1
        elif board[i][i] == " ":
            m = m + 1
    if n == 2 and m == 1:
        return("D1")

    n = 0
    m = 0
    for i in range(3):
        if board[i][2-i] == who:
            n = n + 1
        elif board[i][2-i] == " ":
            m = m + 1
    if n == 2 and m == 1:
        return("D2")

    return None


def check_full():
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False
    return True


def check_3(us, them):
    # rows
    for i in range(3):
        n = 0
        m = 0
        for j in range(3):
            if board[i][j] == us:
                n = n + 1
            elif board[i][j] == them:
                m = m + 1
        if n==3:
            return us
        if m==3:
            return them

    # columns
    for j in range(3):
        n = 0
        m = 0
        for i in range(3):
            if board[i][j] == us:
                n = n + 1
            elif board[i][j] == them:
                m = m + 1
        if n==3:
            return us
        if m==3:
            return them

    n = 0
    m = 0
    for i in range(3):
        if board[i][i] == us:
            n = n + 1
        elif board[i][i] == them:
            m = m + 1
    if n==3:
        return us
    if m==3:
        return them

    n = 0
    m = 0
    for i in range(3):
        if board[i][2-i] == us:
            n = n + 1
        elif board[i][2-i] == them:
            m = m + 1
    if n==3:
        return us
    if m==3:
        return them

    return None


def find_empty(d):
    if d[0] == "R":
        i = int(d[1])
        for j in range(3):
            if board[i][j] == " ":
                return((i,j))
    if d[0] == "C":
        j = int(d[1])
        for i in range(3):
            if board[i][j] == " ":
                return((i,j))

    if d == "D1":
        for i in range(3):
            if board[i][i] == " ":
                return((i,i))
        
    if d == "D2":
        for i in range(3):
            if board[i][2-i] == " ":
                return((i,2-i))

    return((None,None))


def is_empty_center():
    if board[1][1] == " ":
        return True
    else:
        return False
    
def opponent_center_only(them):
    for i in range(3):
        for j in range(3):
            if i==1 and j==1:
                if board[i][j] != them:
                    return False
            else:
                if board[i][j] != " ":
                    return False
    return True


def try_to_make_2(who):
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = who
                result = check_2(who)
                board[i][j] = " "
                if result is not None:
                    return (i,j)
    return (None, None)

def check_last_space_open():
    n = 0
    ii = None
    jj = None
    for i in range(3):
        for j in range(3):
            if board[i][j] != " ":
                n = n + 1
            else:
                ii = i
                jj = j
    if n == 8:
        return(ii,jj)
    return(None, None)


def check_end(us, them):
    # Rule 0 - check for a winner!
    who = check_3(us, them)
    if who == us:
        print("You lose!")
        return True
    elif who == them:
        print("You won!")
        return True
    # Rule 0B - check for a tie!
    if check_full() == True:
        print("It's a tie")
        return True
    return False


def make_move(us, them):
    # Rule 1 - if you can get three in a row, do it
    r1 = check_2(us)
    if r1 is not None:
        i,j = find_empty(r1)
        board[i][j] = us
        return True

    # Rule 2 - if you can block the opponent, do it
    r1 = check_2(them)
    if r1 is not None:
        i,j = find_empty(r1)
        board[i][j] = us
        return True
    
    # Rule 3 - if the center is empty, go there
    if is_empty_center() == True:
        board[1][1] = us
        return True
    
    # Rule 4 - if opponent center only then go in 1,2
    if opponent_center_only(them):
        board[2][2] = us
        return True

    # Rule 5 - try to make 2 in a row
    i,j = try_to_make_2(us)
    if i is not None:
        board[i][j] = us
        return True

    # Rule 6 - if there's only one left, play there
    i,j = check_last_space_open()
    if i is not None:
        board[i][j] = us
        return True
    
    print("Can't make move!")
    return False


def player_makes_move(player):
    i = j = -1
    while(i<0 or j<0):
        print("Enter row (0-2): ")
        i = input()
        i = int(i)
        print("Enter col (0-2): ")
        j = input()
        j = int(j)
        if board[i][j] != " ":
            print("Position taken!")
            i = j = -1
    board[i][j] = player

print("Go first (1) or second (2)?")
x = input()
if(x == "1"):
    player = "X"
    computer = "O"
else:
    player = "O"
    computer = "X"

going = "X"
not_going = "O"

for i in range(10):
    print_board()
    if check_end(going, not_going) == True:
        sys.exit(0)
    print("going = " + going)
    print("player = " + player)
    if player==going:
        player_makes_move(player)
    else:
        if not make_move(computer, player):
            sys.exit(0)
    print_board()
    if going=="X":
        not_going = "X"
        going="O"
    else:
        not_going = "O"
        going="X"

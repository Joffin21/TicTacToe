import sys, tty, termios

class Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

if len(sys.argv) > 1:
    whoAI = sys.argv[1].upper()
    if len(sys.argv) == 3:
        boardState = sys.argv[2]
    else:
        boardState = [".",".",".",".",".",".",".",".","."]
else:
    whoAI = "O"
    boardState = [".",".",".",".",".",".",".",".","."]

def showBoard(game): #Prints the board
    print("\n".join([game[i:i+3] for i in range(0,9,3)]))

def whoTurn(game): #Figures out who's turn it is
    #A faster way would be to count the number of periods. (Do that in a speed up)

    count1,count2 = 0,0
    for each in game:
        if each == "X":
            count1 += 1
        if each == "O":
            count2 +=1
    if count1 == count2:
        return "X"
    else:
        return "O"

def emptySpots(game):
    return {i for i in range(len(game)) if game[i] == "."}

def whoWon(game): #Sees if anybody won.
    #print([game[i:i+3] for i in range(0,9,3)])
    l1 = [[game[i+j] for j in range(0,3)] for i in range(0,9,3)]
    l2 = [[game[(i+(3*j))] for j in range(0,3)] for i in range(0,3)]
    l3 = [[game[0],game[4],game[8]],[game[2],game[4],game[6]]]
    finalL = l1+l2+l3
    for each in finalL:
        if len(set(each)) == 1 and each[0] == "X":
            return "X"
        elif len(set(each)) == 1 and each[0] == "O":
            return "O"
        else:
            continue
    return "."

def partitionMoves(game):
    #showBoard("".join(game))
    #print(game)
    winner = whoWon(game)
    #print(winner)
    mine = whoTurn(game)
    if winner == ".":
        if "." not in game:
            return {},{},{""}
    elif winner != mine and winner != ".":
        return {},{""},{}
    else:
        return {""},{},{}
    good, bad, tie = set(),set(),set()
    moves = emptySpots(game)
    for move in moves:
        #print(move, moves)
        game2 = game[:]
        game2[move] = mine
        tmpGood,tmpBad,tmpTie = partitionMoves(game2)
        if tmpGood:
            bad.add(move)
        elif tmpTie:
            tie.add(move)
        else:
            good.add(move)
    #print("")
    #print((good,bad,tie),mine)
    return good, bad, tie

#print(whoWon(["X","X","X","O","O",".",".",".","."]))
#How to respond immediately to an input.

game = boardState
showBoard("".join(game))
mine = whoAI
if mine == "X":
    notMine = "O"
else:
    notMine = "X"
check = 0
while("." in game):
    if(whoWon(game) == mine):
        print("You Won")
        check = 1
        break
    elif(whoWon(game) == notMine):
        print("Computer Won")
        check = 1
        break
    else:
        if whoTurn(game) == mine:
            spots = emptySpots(game)
            spots  = sorted([str(each) for each in spots])
            print("Possible moves are: ", end = "")
            print(spots)
            print("What is your move? ", end = "", flush=True)
            inkey = Getch()
            k=inkey()
            print(k)
            # while k<"0" or k>"8":
            #     print("Please input a number between 0-8 ", end = "", flush = True)
            #     k=inkey()
            #     print(k)
            #     if k == "0" or k == "1" or k == "2" or k == "3" or k == "4" or k == "5" or k == "6" or k == "7" or k == "8":
            #         k = int(k)
            #         if game[k] != ".":
            #             print("Please make sure the inputted value is on an empty space.")
            #             print("Possible moves are: ", end = "")
            #             print(emptySpots(game))
            #             k = inkey()
            #     k = str(k)
            if k == "Q":
                "Goodbye!"
                exit()
            while k not in spots:
                print("")
                print("Please input a number between 0-8 and make sure it is a possible move.")
                print("Possible moves are: ", end = "")
                print(spots)
                print("What is your move? ", end = "", flush=True)
                inkey = Getch()
                k=inkey()
                print(k)
            k = int(k)
            game[k] = mine
        else:
            print("")
            good, bad, tie = partitionMoves(game)
            if len(good) > 0:
                game[good.pop()] = notMine
            elif len(tie) > 0:
                game[tie.pop()] = notMine
            elif len(bad) > 0:
                game[bad.pop()] = notMine
    showBoard("".join(game))
if check == 0:
    print("It's a tie")

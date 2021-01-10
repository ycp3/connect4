import math
import random
from copy import deepcopy
import os

firstmove = [[" "] * 7 for _ in range(5)]
firstmove.append([" ", " ", " ", "X", " ", " ", " "])

class Board:
    def __init__(self, matrix=[[" "] * 7 for _ in range(6)]):
        self.matrix = matrix

    def draw(self):
        for row in range(6):
            print("|", end="")
            for col in range(7):
                if col == 6:
                    print(self.matrix[row][col], end="")
                else:
                    print(self.matrix[row][col], end=" ")
            print("|")
        print("\u0305".join(" 1 2 3 4 5 6 7"))

    def draw_winner(self, coords, direction):
        x = coords[0]
        y = coords[1]
        winner_matrix = [[" "] * 7 for _ in range(6)]
        winner_matrix[x][y] = self.matrix[x][y]
        if direction == "r":
            winner_matrix[x+1][y] = winner_matrix[x][y]
            winner_matrix[x+2][y] = winner_matrix[x][y]
            winner_matrix[x+3][y] = winner_matrix[x][y]
        elif direction == "d":
            winner_matrix[x][y+1] = winner_matrix[x][y]
            winner_matrix[x][y+2] = winner_matrix[x][y]
            winner_matrix[x][y+3] = winner_matrix[x][y]
        elif direction == "dr":
            winner_matrix[x+1][y+1] = winner_matrix[x][y]
            winner_matrix[x+2][y+2] = winner_matrix[x][y]
            winner_matrix[x+3][y+3] = winner_matrix[x][y]
        elif direction == "dl":
            winner_matrix[x-1][y+1] = winner_matrix[x][y]
            winner_matrix[x-2][y+2] = winner_matrix[x][y]
            winner_matrix[x-3][y+3] = winner_matrix[x][y]
        for row in range(6):
            print("|", end="")
            for col in range(7):
                if col == 6:
                    print(self.matrix[row][col], end="")
                else:
                    print(self.matrix[row][col], end=" ")
            print("|    |", end="")
            for col in range(7):
                if col == 6:
                    print(winner_matrix[row][col], end="")
                else:
                    print(winner_matrix[row][col], end=" ")
            print("|")
        print("\u0305".join(" 1 2 3 4 5 6 7"), end="     ")
        print("\u0305".join(" 1 2 3 4 5 6 7"))

    def check_winner(self):
        for row in range(6):
            for col in range(4):
                if (
                    self.matrix[row][col] != " "
                    and self.matrix[row][col] == self.matrix[row][col+1]
                    and self.matrix[row][col] == self.matrix[row][col+2]
                    and self.matrix[row][col] == self.matrix[row][col+3]
                ):
                    return [True, self.matrix[row][col], [row, col], "d"]
        for row in range(3):
            for col in range(7):
                if (
                    self.matrix[row][col] != " "
                    and self.matrix[row][col] == self.matrix[row+1][col]
                    and self.matrix[row][col] == self.matrix[row+2][col]
                    and self.matrix[row][col] == self.matrix[row+3][col]
                ):
                    return [True, self.matrix[row][col], [row, col], "r"]
        for row in range(3):
            for col in range(4):
                if (
                    self.matrix[row][col] != " "
                    and self.matrix[row][col] == self.matrix[row+1][col+1]
                    and self.matrix[row][col] == self.matrix[row+2][col+2]
                    and self.matrix[row][col] == self.matrix[row+3][col+3]
                ):
                    return [True, self.matrix[row][col], [row, col], "dr"]
        for row in range(3, 6):
            for col in range(4):
                if (
                    self.matrix[row][col] != " "
                    and self.matrix[row][col] == self.matrix[row-1][col+1]
                    and self.matrix[row][col] == self.matrix[row-2][col+2]
                    and self.matrix[row][col] == self.matrix[row-3][col+3]
                ):
                    return [True, self.matrix[row][col], [row, col], "dl"]
        if not " " in self.matrix[0]:
            return [True, None]
        return [False, None]

    def current_player(self):
        count = 0
        for row in self.matrix:
            for col in row:
                if col != " ":
                    count += 1
        if count % 2 == 0:
            return "X"
        return "O"

    def play(self, col):
        i = 5
        col -= 1
        while(self.matrix[i][col] != " "):
            i -= 1
            if i < 0:
                return False
        self.matrix[i][col] = self.current_player()
        return True

    def legal_moves(self):
        possible_moves = []
        for i in range(7):
            if self.matrix[0][i] == " ":
                possible_moves.append(i+1)
        return possible_moves

    def find_three(self, char):
        for row in range(6):
            for col in range(5):
                if(
                    self.matrix[row][col] == char
                    and self.matrix[row][col+1] == char
                    and self.matrix[row][col+2] == char
                ):
                    if(
                        col != 4 and self.matrix[row][col+3] == " "
                        and (row == 5 or self.matrix[row+1][col+3] != " ")
                    ):
                        return [True, col+3]
                    elif(
                        col != 0 and self.matrix[row][col-1] == " "
                        and (row == 5 or self.matrix[row+1][col-1] != " ")
                    ):
                        return [True, col-1]
        for row in range(4):
            for col in range(7):
                if(
                    self.matrix[row][col] == char
                    and self.matrix[row+1][col] == char
                    and self.matrix[row+2][col] == char
                ):
                    if(
                        row != 0 and self.matrix[row-1][col] == " "
                    ):
                        return [True, col]
        for row in range(4):
            for col in range(5):
                if(
                    self.matrix[row][col] == char
                    and self.matrix[row+1][col+1] == char
                    and self.matrix[row+2][col+2] == char
                ):
                    if(
                        row != 0 and col != 0
                        and self.matrix[row-1][col-1] == " "
                        and self.matrix[row][col-1] != " "
                    ):
                        return [True, col-1]
                    elif(
                        row != 3 and col != 4
                        and self.matrix[row+3][col+3] == " "
                        and (row == 2 or self.matrix[row+4][col+3] != " ")
                    ):
                        return [True, col+3]
        for row in range(4):
            for col in range(2, 7):
                if(
                    self.matrix[row][col] == char
                    and self.matrix[row+1][col-1] == char
                    and self.matrix[row+2][col-2] == char
                ):
                    if(
                        row != 0 and col != 6
                        and self.matrix[row-1][col+1] == " "
                        and self.matrix[row][col+1] != " "
                    ):
                        return [True, col+1]
                    elif(
                        row != 3 and col != 2
                        and self.matrix[row+3][col-3] == " "
                        and (row == 2 or self.matrix[row+4][col-3] != " ")
                    ):
                        return [True, col-3]
        for row in range(6):
            for col in range(4):
                if(
                    self.matrix[row][col] == char
                    and self.matrix[row][col+1] == char
                    and self.matrix[row][col+3] == char
                    and self.matrix[row][col+2] == " "
                    and (row == 5 or self.matrix[row+1][col+2] != " ")
                ):
                    return [True, col+2]
                elif(
                    self.matrix[row][col] == char
                    and self.matrix[row][col+2] == char
                    and self.matrix[row][col+3] == char
                    and self.matrix[row][col+1] == " "
                    and (row == 5 or self.matrix[row+1][col+1] != " ")
                ):
                    return [True, col+1]
        for row in range(3):
            for col in range(4):
                if(
                    self.matrix[row][col] == char
                    and self.matrix[row+1][col+1] == char
                    and self.matrix[row+3][col+3] == char
                    and self.matrix[row+2][col+2] == " "
                    and self.matrix[row+3][col+2] != " "
                ):
                    return [True, col+2]
                elif(
                    self.matrix[row][col] == char
                    and self.matrix[row+2][col+2] == char
                    and self.matrix[row+3][col+3] == char
                    and self.matrix[row+1][col+1] == " "
                    and self.matrix[row+2][col+1] != " "
                ):
                    return [True, col+1]
        for row in range(3, 6):
            for col in range(4):
                if(
                    self.matrix[row][col] == char
                    and self.matrix[row-1][col+1] == char
                    and self.matrix[row-3][col+3] == char
                    and self.matrix[row-2][col+2] == " "
                    and self.matrix[row-1][col+2] != " "
                ):
                    return [True, col+2]
                elif(
                    self.matrix[row][col] == char
                    and self.matrix[row-2][col+2] == char
                    and self.matrix[row-3][col+3] == char
                    and self.matrix[row-1][col+1] == " "
                    and self.matrix[row][col+1] != " "
                ):
                    return [True, col+1]
        for row in range(6):
            for col in range(3):
                if(
                    self.matrix[row][col] == " "
                    and self.matrix[row][col+1] == char
                    and self.matrix[row][col+2] == " "
                    and self.matrix[row][col+3] == char
                    and self.matrix[row][col+4] == " "
                    and (row == 5 or (
                        self.matrix[row+1][col] != " "
                        and self.matrix[row+1][col+2] != " "
                        and self.matrix[row+1][col+4] != " "
                    ))
                ):
                    return [True, col+2]
        for row in range(2):
            for col in range(3):
                if(
                    self.matrix[row][col] == " "
                    and self.matrix[row+1][col+1] == char
                    and self.matrix[row+2][col+2] == " "
                    and self.matrix[row+3][col+3] == char
                    and self.matrix[row+4][col+4] == " "
                    and self.matrix[row+1][col] != " "
                    and self.matrix[row+3][col+2] != " "
                    and (row == 1 or self.matrix[row+5][col+4] != " ")
                ):
                    return [True, col+2]
        for row in range(4, 6):
            for col in range(3):
                if(
                    self.matrix[row][col] == " "
                    and self.matrix[row-1][col+1] == char
                    and self.matrix[row-2][col+2] == " "
                    and self.matrix[row-3][col+3] == char
                    and self.matrix[row-4][col+4] == " "
                    and (row == 5 or self.matrix[row+1][col] != " ")
                    and self.matrix[row-1][col+2] != " "
                    and self.matrix[row-3][col+4] != " "
                ):
                    return [True, col+2]
        return [False]


class Bot:
    def __init__(self, char):
        self.char = char
        self.tree = None

    def simulate(self, state):
        simboard = Board(state)
        simwinner = simboard.check_winner()
        while(not simwinner[0]):
            simboard.play(random.choice(simboard.legal_moves()))
            simwinner = simboard.check_winner()
        return simwinner

    def augment_state(self, state, move):
        simboardd = Board(state)
        simboardd.play(move)
        return simboardd.matrix

    def backpropagate(self, node, amount):
        if node.parent == None:
            node.visited += 1
        else:
            node.visited += 1
            node.wins += amount
            self.backpropagate(node.parent, amount)

    def UBT_select(self, node):
        children = node.children
        child_values = {}
        for child in children:
            if child.visited == 0:
                child_values[child] = math.inf
            else:
                child_values[child] = (
                    child.wins / child.visited
                    + child.c * math.sqrt(math.log(child.parent.visited) / child.visited)
                )
        
        val = max(child_values, key=child_values.get)
        return val

    def create_tree(self, state):
        self.tree = Node(state)

    def get_child(self, tree):
        if tree.children == None:
            return tree
        else:
            return self.get_child(self.UBT_select(tree))

    def select_move(self, iterations):
        for _ in range(iterations):
            cnode = self.get_child(self.tree)
            cboard = Board(cnode.state)
            if cnode.children == None:
                cnode.children = []
            if len(cboard.legal_moves()) != 0:
                cnode.children = []
                initial = deepcopy(cnode.state)
                for move in cboard.legal_moves():
                    cnode.children.append(
                        Node(self.augment_state(cnode.state, move), parent=cnode)
                        )
                    cnode.state = deepcopy(initial)
            simnode = random.choice(cnode.children)
            siminitial = deepcopy(simnode.state)
            result = self.simulate(simnode.state)
            simnode.state = deepcopy(siminitial)
            if result[1] == self.char:
                self.backpropagate(simnode, 1)
            elif result[1] == None:
                self.backpropagate(simnode, 0)
            else:
                self.backpropagate(simnode, 0)
        child_visits = {}
        for child in self.tree.children:
            child_visits[child] = child.visited
        choice = max(child_visits, key=child_visits.get)
        try:
            print("Bot confidence: {:.1f}%".format((choice.wins / choice.visited) * 100))
        except:
            print("Bot is not confident")
        return choice.state

    def block(self, state):
        if bot.char == "X":
            player = "O"
        else:
            player = "X"
        getmoves = Board(state)
        return getmoves.find_three(player)


class Node:
    def __init__(self, state, children=None, parent=None):
        self.state = state
        self.visited = 0
        self.wins = 0
        self.c = math.sqrt(2)
        self.parent = parent
        self.leaf = None
        self.children = None
        if children == None:
            self.leaf == True
        else:
            self.leaf == False
            self.children = children

print("Choose a mode:")
print("    1 - vs AI")
print("    2 - vs Player")
mode = 0
while(not (mode == 1 or mode == 2)):
    try:
        mode = int(input())
    except:
        print("Please enter a valid option")

board = Board()

if mode == 1:
    print("Choose bot difficulty:")
    print("    1-inf, random-hard")
    print("    the larger the value (>10000), the slower the game")
    diff = 0
    while(not (diff >= 1)):
        try:
            diff = int(input())
        except:
            print("Please enter a valid number")
    print("Chose a side:")
    print("    1 - X")
    print("    2 - O")
    pchar = 0
    while(not (pchar == 1 or pchar == 2)):
        try:
            pchar = int(input())
        except:
            print("Please enter a valid option")
    if pchar == 1:
        bot = Bot("O")
    else:
        bot = Bot("X")
    winner = [False]
    while(not winner[0]):
        if board.current_player() == bot.char:
            if(
                bot.char == "O"
                and board.matrix == firstmove
            ):
                board.play(4)
                winner = board.check_winner()
                print("Bot: First move counter")
                continue
            blocktest = bot.block(board.matrix)
            if blocktest[0]:
                board.play(blocktest[1]+1)
                winner = board.check_winner()
                print("Bot: Blocked")
                continue
            board.draw()
            print(f"\nCurrent player: {board.current_player()}")
            print("Please wait")
            bot.create_tree(board.matrix)
            board.matrix = bot.select_move(diff)
        else:
            board.draw()
            print(f"\nCurrent player: {board.current_player()}")
            print("Choose column:")
            move = 0
            while(move < 1 or move > 7):
                try:
                    move = int(input())
                    if move == -1:
                        os._exit(0)
                    if move < 1 or move > 7:
                        raise ValueError
                except:
                    print("Please enter a number from 1-7")
            if not board.play(move):
                print("Invalid move")
        winner = board.check_winner()
else:
    winner = [False]
    while(not winner[0]):
        board.draw()
        print(f"\nCurrent player: {board.current_player()}")
        print("Choose column:\n")
        move = 0
        while(move < 1 or move > 7):
            try:
                move = int(input())
                if move < 1 or move > 7:
                    raise ValueError
            except:
                print("Please enter a number from 1-7")
        if not board.play(move):
            print("Invalid move")
        winner = board.check_winner()
if winner[1] == None:
    board.draw()
    print("\nDraw!")
else:
    board.draw_winner(winner[2], winner[3])
    print(f"\n{winner[1]} wins!")
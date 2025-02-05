import random

moves = ["R","P","S"]
move = moves.index(random.choice(moves))

while True:
    print(moves[move])
    move = moves.index(input())
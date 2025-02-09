import random
input()

moves = ["R","P","S"]
move = moves.index(random.choice(moves))

while True:
    print(moves[move])
    input()
    move=(move+1)%3
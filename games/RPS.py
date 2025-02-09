import zudge
from sys import argv

#file managment

if len(argv)<3:
    print("Usage: python RPS.py <player1> <player2> [<output file>] [<number of rounds>]")
    exit(1)
p = zudge.start(argv[1:3])

if len(argv)>=4:
    zudge.open(argv[3])

rounds: int = 10
if len(argv)>=5:
    rounds = int(argv[4])

#game parts

score: list[int] = [0,0]
move: list[str] = ["",""]
moves: list[str] = ["R","P","S"]
beats: dict[str,str] = {
    "R":"P",
    "P":"S",
    "S":"R"
}

zudge.print(f"p0: {argv[1]}")
zudge.print(f"p1: {argv[2]}")

def disqualify(i:int):
    if i==2:
        zudge.print("BOTH DISUALIFIED")
        finalize()
    zudge.print(f"p{i} DISQUALIFIED")
    score[1-i] += score[i] + 1
    finalize()

def finalize():
    zudge.print("\n\n")
    zudge.print(f"p0: {score[0]}\t{argv[1]}")
    zudge.print(f"p1: {score[1]}\t{argv[2]}")
    if score[0]==score[1]:
        zudge.print("DRAW")
    else:
        zudge.print(argv[1 if score[0]>score[1] else 2])
    exit(0)

def ask():
    move[0] = zudge.read(p[0])
    move[1] = zudge.read(p[1])
    if move[0] is None and move[1] is None:
        disqualify(2)
    if move[0] is None:
        disqualify(0)
    if move[1] is None:
        disqualify(1)

def judge():
    if (move[0] not in moves) and (move[1] not in moves):
        disqualify(2)
    if move[0] not in moves:
        disqualify(0)
    if move[1] not in moves:
        disqualify(1)
    if move[0] == move[1]:
        zudge.print("dr"," ")
    elif move[0] == beats[move[1]]:
        zudge.print("p0"," ")
        score[0] += 1
    elif move[1] == beats[move[0]]:
        zudge.print("p1"," ")
        score[1] += 1

def tell():
    zudge.write(p[0],move[1])
    zudge.write(p[1],move[0])

#game

zudge.write(p,rounds)

for _ in range(rounds):
    ask()
    judge()
    tell()

finalize()
import zudge
from sys import argv

#file managment

if len(argv)<3:
    print("Usage: python RPS2.py <player1> <player2> [<number of rounds>] [<output file>]")
    exit(1)
p = zudge.start(argv[1:3])

if len(argv)>=4:
    rounds = int(argv[3])

rounds: int = 10
if len(argv)>=5:
    zudge.open(argv[4])

#functions and variables

score = [0,0]
hands = ["",""]
moves = ["",""]

beats = {
    "R":"P",
    "P":"S",
    "S":"R"
}

def finalize():
    zudge.print("\n\n")
    zudge.print(f"p0: {score[0]}\t{argv[1]}")
    zudge.print(f"p1: {score[1]}\t{argv[2]}")
    if score[0]==score[1]:
        zudge.print("DRAW")
    else:
        zudge.print(argv[1 if score[0]>score[1] else 2])
    exit(0)

def disqualify(i:int):
    if i==2:
        zudge.print("BOTH DISQUALIFIED")
        finalize()
    zudge.print(f"p{i} DISQUALIFIED")
    score[1-i] += score[i]+1
    finalize()

def qualify_hand(hand:str|None)->bool:
    if hand is None:
        return False
    if len(hand) != 2:
        return False
    for i in hand:
        if i not in beats:
            return False
    return True

def gethands():
    global hands
    hands = zudge.read(p)

def qualifyhands():
    h0 = qualify_hand(hands[0])
    h1 = qualify_hand(hands[1])
    if (not h0) and (not h1):
        disqualify(2)
    if not h0:
        disqualify(0)
    if not h1:
        disqualify(1)

def tellhands():
	zudge.write(p[0],hands[1])
	zudge.write(p[1],hands[0])

def getmoves():
    global moves
    moves = zudge.read(p)

def qualifymoves():
    m0 = moves[0] in hands[0]
    m1 = moves[1] in hands[1]
    if (not m0) and (not m1):
        disqualify(2)
    if not m0:
        disqualify(0)
    if not m1:
        disqualify(1)

def judge():
    if moves[0] == moves[1]:
        zudge.print("dr"," ")
    elif moves[0] == beats[moves[1]]:
        zudge.print("p0"," ")
        score[0] += 1
    elif moves[1] == beats[moves[0]]:
        zudge.print("p1"," ")
        score[1] += 1

def tellmoves():
    zudge.write(p[0],moves[1])
    zudge.write(p[1],moves[0])

#game

zudge.print(f"p0: {argv[1]}")
zudge.print(f"p1: {argv[2]}")

zudge.write(p,rounds)
for _ in range(rounds):
    gethands()
    qualifyhands()
    tellhands()
    getmoves()
    qualifymoves()
    judge()
    tellmoves()

finalize()
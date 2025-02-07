import zudge
import sys

#file managment

if len(sys.argv)<3:
    print("Usage: python RPS.py <player1> <player2> [<output file>]")
    exit(1)
p = zudge.start(sys.argv[1:3])

if len(sys.argv)>=4:
    zudge.open(sys.argv[3])

#GAME!!!

def disqualify(p:int):
    zudge.print(f"p{p} \"{sys.argv[p]}\" is disqualified")
    zudge.print(f"p{3-p} \"{sys.argv[3-p]}\" wins!")
    exit(0)

def judge(p1move:int,p2move:int)->None:
    if p1move==p2move:
        zudge.print("draw!")
        return None
    if p1move==(p2move+1)%3:
        zudge.print(f"p1 \"{sys.argv[1]}\" wins!")
        return None
    zudge.print(f"p2 \"{sys.argv[2]}\" wins!")
    return None

moves = ["R","P","S"]

for _ in range(10):
    p1move = zudge.read(p[0])
    p2move = zudge.read(p[1])
    if p1move is None and p2move is None:
        zudge.print("both players disqualified")
        zudge.print("draw!")
        exit(0)
    if p1move is None:
        disqualify(1)
    if p2move is None:
        disqualify(2)
    p1illegal = p1move not in moves
    p2illegal = p2move not in moves
    if p1illegal and p2illegal:
        zudge.print("both players disqualified")
        zudge.print("draw!")
        exit(0)
    if p1illegal:
        disqualify(1)
    if p2illegal:
        disqualify(2)
    judge(moves.index(p1move),moves.index(p2move))
    zudge.write(p[0],p2move)
    zudge.write(p[1],p1move)

print("\n\nDONE!")
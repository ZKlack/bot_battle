import zudge

#open output file if provided
FILE = None
if len(zudge.sys.argv) >= 4:
    FILE = open(zudge.sys.argv[3],mode="w")
    zudge.atexit.register(lambda: FILE.close())

#write function to handle if the output is on the terminal or a file
def write(txt:str, end:str="\n"):
    if FILE is not None:
        return FILE.write(txt+end)
    print(txt,end=end)
    return 0

#check that players are online
if zudge.p1.poll() is not None:
    print("p1 is offline")
    exit(1)
if zudge.p2.poll() is not None:
    print("p2 is offline")
    exit(1)

#
#
#GAME!!!
#
#

def disqualify(p:int):
    write(f"p{p} \"{zudge.sys.argv[p]}\" is disqualified")
    write(f"p{3-p} \"{zudge.sys.argv[3-p]}\" wins!")
    exit(0)

def judge(p1move:int,p2move:int)->None:
    if p1move==p2move:
        write("draw!")
        return None
    if p1move==(p2move+1)%3:
        write(f"p1 \"{zudge.sys.argv[1]}\" wins!")
        return None
    write(f"p2 \"{zudge.sys.argv[2]}\" wins!")
    return None

moves = ["R","P","S"]

for _ in range(10):
    p1move = zudge.read(zudge.p1)
    p2move = zudge.read(zudge.p2)
    if p1move is None and p2move is None:
        write("both players disqualified")
        write("draw!")
        exit(0)
    if p1move is None:
        disqualify(1)
    if p2move is None:
        disqualify(2)
    p1illegal = p1move not in moves
    p2illegal = p2move not in moves
    if p1illegal and p2illegal:
        write("both players disqualified")
        write("draw!")
        exit(0)
    if p1illegal:
        disqualify(1)
    if p2illegal:
        disqualify(2)
    judge(moves.index(p1move),moves.index(p2move))
    zudge.write(zudge.p1,p2move)
    zudge.write(zudge.p2,p1move)

print("\n\nDONE!")
import zudge
import sys

#file managment

if len(sys.argv)<3:
    print("Usage: python RPS.py <player1> <player2> [<output file>] [<number of matches>]")
    exit(1)
p = zudge.start(sys.argv[1:3])

if len(sys.argv)>=4:
    zudge.open(sys.argv[3])

#GAME!!!

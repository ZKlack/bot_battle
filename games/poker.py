import zudge
from sys import argv

#utility
def argerror(txt:str=""):
	print(txt,end="" if txt=="" else "\n")
	print("Usage: python poker.py <player0> <player1> [-f <file name>] [-r <round count>]")
	exit(1)

#cmd setup
players = []
rounds = 10
p = []

while len(argv)>0:
	if argv[0].startswith("-"):
		if argv[0]=="-f":
			if zudge.FILE is not None:
				argerror("Error: there can only be one \"-f\" flag")
			if len(argv)<2:
				argerror("Error: a file name must be provided after \"-f\"")
			zudge.open(argv[1])
			argv = argv[2:]
			continue
		if argv[0]=="-r":
			if len(argv)<2:
				argerror("Error: a round count must be provided after \"-r\"")
			rounds = int(argv[1])
			argv = argv[2:]
			continue
	players.append(argv[0])
	argv = argv[1:]

p = zudge.start(players)
zudge.write(p,rounds)
for i in range(len(players)):
	zudge.print(f"p{i}: {players[i]}\n")


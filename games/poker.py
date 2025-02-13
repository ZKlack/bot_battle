import zudge
from sys import argv
import random

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

if not 2<=len(players)<=6:
	argerror("Error: players must be 2 to 6")

p = zudge.start(players)
zudge.write(p,rounds)
zudge.write(p,len(players))
for i in range(len(players)):
	zudge.write(p[i],i)
	zudge.print(f"p{i}: {players[i]}\n")

#game util

def deal(deck:list[str],N:int=1):
	cards = random.sample(deck,N)
	for card in cards:
		deck.remove(card)
	return cards

#game setup

sampledeck = [rank+suit for rank in "A23456789TJQK" for suit in "DSCH"]
score = [0 for _ in p]

#gameloop

for _ in range(rounds):
	chips = [60 for _ in p]
	pool=0
	deck = sampledeck.copy()
	hands = [deal(deck,2) for _ in p]
	for i in range(len(hands)):
		for card in hands[i]:
			zudge.write(p[i],card)
	community = deal(deck,5)
	plays = [[] for _ in p]
	zudge.write(p,community[0])
	zudge.write(p,community[1])
	for i in range(2,5):
		for j in range(len(p)):
			if len(plays[j])>0 and plays[j][-1] in ["ALL","fold","disq"]:
				continue
			plays[j].append(zudge.read(p[j]))
			#qualify move
			if plays[j][-1] is None:
				plays[j][-1] = "disq"
			elif plays[j][-1] not in ["ALL","fold","raise"]:
				plays[j][-1] = "disq"
			#execute move
			if plays[j][-1]=="ALL":
				pool+=chips[j]
				chips[j]=0
			elif plays[j][-1]=="raise":
				pool+=10
				chips[j]-=10

		zudge.write(p,community[i])
		for j in range(len(p)):
			zudge.write(p,f"{j} {plays[j][-1]}")
	handrank=[0 for _ in p]
	for i in range(len(p)):
		if plays[i][-1] in ["fold","disq"]:
			handrank=-1
			continue
		hands[i]+=community
		# TODO: I'm lost, how can I set the gand rank? seems complicated; will do on pen and paper first
	# TODO: take highest rank and sort them on value
	# TODO: distrubute "pool" between the highest value of the highest rank in "score" (most likely one person)
# TODO: list total points "score" (zudge.print)
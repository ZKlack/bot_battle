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

argv=argv[1:]
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
	zudge.print(f"p{i}: {players[i]}")

#game util

def deal(deck:list[str],N:int=1):
	cards = random.sample(deck,N)
	for card in cards:
		deck.remove(card)
	return cards

def isroyalflush(hand:list[str])->bool:
	big_ranks = { "T", "J", "Q", "K", "A" }
	suits = { suit:set() for suit in "DSCH" }
	for card in hand:
		if card[0] in big_ranks:
			suits[card[1]].add(card[0])
	return any([big_ranks<=suits[suit] for suit in "DSCH"])

def isstraightflush(hand:list[str])->bool:
	rank_order = "A23456789TJQKA"
	suits = { suit:set() for suit in "DSCH" }
	for card in hand:
		suits[card[1]].add(card[0])
	return any([set(rank_order[i:i+5])<=suits[suit] for i in range(len(rank_order)-5) for suit in "DSCH"])

def isfourofakind(hand:list[str])->bool:
	rank_counts = { rank:0 for rank in "A23456789TJQK" }
	for card in hand:
		rank_counts[card[0]]+=1
	return any([ rank_counts[rank]>=4 for rank in "A23456789TJQK" ])

def isfullhouse(hand:list[str])->bool:
	rank_counts = { rank:0 for rank in "A23456789TJQK" }
	for card in hand:
		rank_counts[card[0]]+=1
	counts = sorted(rank_counts.values(),reverse=True)
	return counts[0]>=3 and counts[1]>=2

def isflush(hand:list[str])->bool:
	suit_counts = { suit:0 for suit in "DSCH" }
	for card in hand:
		suit_counts[card[1]]+=1
	return any([ count>=5 for count in suit_counts.values() ])

def isstraight(hand:list[str])->bool:
	rank_order = "A23456789TJQKA"
	ranks = set()
	for card in hand:
		ranks.add(card[0])
	return any([ set(rank_order[i:i+5])<=ranks for i in range(len(rank_order)-5)])

def isthreeofakind(hand:list[str])->bool:
	rank_counts = { rank:0 for rank in "A23456789TJQK" }
	for card in hand:
		rank_counts[card[0]]+=1
	return any([ count>=3 for count in rank_counts.values() ])

def istwopair(hand:list[str])->bool:
	rank_counts = { rank:0 for rank in "A23456789TJQK" }
	for card in hand:
		rank_counts[card[0]]+=1
	counts = sorted(rank_counts.values(),reverse=True)
	return counts[1]>=2

def isonepair(hand:list[str])->bool:
	seen_ranks = set()
	for card in hand:
		if card[0] in seen_ranks:
			return True
		seen_ranks.add(card[0])
	return False

def judgehand(hand:list[str])->int:
	cardeval="__23456789TJQKA"
	return sum([ cardeval.index(card[0]) for card in hand ])

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
			zudge.write(p,f"{j}\n{plays[j][-1]}")
	handrank={i:"disq" for i in range(len(p))}
	for i in range(len(p)):
		if plays[i][-1] in ["fold","disq"]:
			continue
		hands[i]+=community.copy()
		if	 isroyalflush(hands[i]):		handrank[i]="royal flush"
		elif isstraightflush(hands[i]):		handrank[i]="straight flush"
		elif isfourofakind(hands[i]):		handrank[i]="four of a kind"
		elif isfullhouse(hands[i]):			handrank[i]="full house"
		elif isflush(hands[i]):				handrank[i]="flush"
		elif isstraight(hands[i]):			handrank[i]="straight"
		elif isthreeofakind(hands[i]):		handrank[i]="three of a kind"
		elif istwopair(hands[i]):			handrank[i]="two pair"
		elif isonepair(hands[i]):			handrank[i]="one pair"
		else:								handrank[i]="high card"
	hand_priority = ["royal flush", "straight flush", "four of a kind", "full house", "flush", "straight", "three of a kind", "two pair", "one pair", "high card"]
	highestrank = hand_priority[-1]
	highesthands:dict[int,int]={}
	for i,rank in handrank.items():
		if rank in hand_priority:
			if hand_priority.index(rank) < hand_priority.index(highestrank):
				highestrank=rank
				highesthands={i:judgehand(hands[i])}
			elif rank==highestrank:
				highesthands[i]=judgehand(hands[i])
	winners = [ i for i,points in highesthands.items() if points==max(highesthands.values()) ]
	zudge.print("[",end="")
	for i in winners:
		score[i]+=pool//len(winners)
		zudge.print(f" p{i}",end="")
	zudge.print(" ] ",end="")
zudge.print("\n\n")
for i in range(len(p)):
	zudge.print(f"p{i}: {score[i]}\t\t{players[i]}")
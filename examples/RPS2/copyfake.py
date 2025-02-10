import random
input()

hands = ["RP","RS","PS"]
nxt = ["  "," "]
nxt[0] = random.choice(hands)
nxt[1] = random.choice(nxt[0])
while True:
	print(nxt[0])
	hand = input()
	print(nxt[1])
	move = input()
	nxt = [hand,hand[0] if move==hand[1] else hand[1]]
	
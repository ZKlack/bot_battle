import random
input()

hands = ["RP","RS","PS"]
choice = {
	"RP" : {
		str(sorted("RP")): "P",
		str(sorted("RS")): "P",
		str(sorted("PS")): "R",
		str(sorted("RR")): "P",
		str(sorted("PP")): "P",
		str(sorted("SS")): "R"
	},
	"RS" : {
		str(sorted("RP")): "S",
		str(sorted("RS")): "R",
		str(sorted("PS")): "R",
		str(sorted("RR")): "R",
		str(sorted("PP")): "S",
		str(sorted("SS")): "R"
	},
	"PS" : {
		str(sorted("RP")): "S",
		str(sorted("RS")): "P",
		str(sorted("PS")): "S",
		str(sorted("RR")): "P",
		str(sorted("PP")): "S",
		str(sorted("SS")): "S"
	}
}

while True:
	hand = random.choice(hands)
	print(hand)
	other = str(sorted(input()))
	print(choice[hand][other])
	input()
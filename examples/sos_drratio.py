import random
input()

moves = {
    "split":10,
    "steal":10
}

while True:
    print(random.choices(["split","steal"],[moves["split"],moves["steal"]])[0])
    moves[input()]+=1
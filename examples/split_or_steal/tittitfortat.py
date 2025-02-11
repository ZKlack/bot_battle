input()
print("split")
tat = 0
while True:
    if input()=="steal":
        tat+=2
    if tat>0:
        print("steal")
        tat-=1
    else:
        print("split")
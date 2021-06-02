import random
n = 100000
count = 0
for x in range(n):
    l = []
    for x in range(50):
        if x<=14:
            l.append(True)
        else:
            l.append(False)

    p2 = 0
    for x in range(16):
        if l.pop(random.randint(0,len(l)-1)):
            p2 += 1

    p1 = (14-p2)/34
    p2 = p2/16

    if p1-p2 >= 0.04:
        count += 1

print(count/n)
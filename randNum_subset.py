import random

def genRandSubSet(n,k):
    result =[]
    for i in range(k):
        randNum= random.randrange(n)
        result.append(randNum)
    return result
print(genRandSubSet(100,4))
import random

def genRandSubSet(n,k):
    #Just a random number generator from set n for k times
    #ALLOWS DUPLICATES
    result =[]
    for i in range(k):
        randNum= random.randrange(n)
        result.append(randNum)
    return result
print(genRandSubSet(3,4))


def random_subset(n: int, k: int):

    if k > n:
        return (f"Error: {k} is a subset size must be smaller than the set n")

    #Uniform random subset of size k from {0..n-1}
    #(AKA LIKE A DECK OF CARDS, ALL CARDS HAVE EQUAL CHANCE OF BEING CHOSEN)
    #O(k) time / O(k) extra space.

    changed = {}  #maps index to value actually stored there
    for i in range(k):
        r = random.randrange(i, n)  #chooses partner to swap with i  

        #logical values currently at i and r
        val_r = changed.get(r, r)
        val_i = changed.get(i, i)

        #perform the logical swap
        changed[i] = val_r
        changed[r] = val_i
    print(changed)

    return [changed[i] for i in range(k)]

print(random_subset(3, 4))   #tests
print(random_subset(1000000, 5))  

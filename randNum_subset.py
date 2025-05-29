import random

def genRandSubSet(n,k):
    result =[]
    for i in range(k):
        randNum= random.randrange(n)
        result.append(randNum)
    return result
print(genRandSubSet(100,4))


def random_subset(n: int, k: int):

    #Uniform random subset of size k from {0..n-1}
    #O(k) time / O(k) extra space.

    changed = {}                    #maps index to value actually stored there
    for i in range(k):
        r = random.randrange(i, n)  #chooses partner to swap with i  

        #logical values currently at i and r
        val_r = changed.get(r, r)
        val_i = changed.get(i, i)

        #perform the logical swap
        changed[i] = val_r
        changed[r] = val_i

    return [changed[i] for i in range(k)]

print(random_subset(5, 3))   #tests
print(random_subset(1000000, 5))  

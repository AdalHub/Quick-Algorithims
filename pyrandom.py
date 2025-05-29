
import random
import time
b = [1000, 100 , 1, -1]
x = random.random()
for i in b:
    time.sleep(5)
    random.shuffle(b)
    print(i)
    print(b)

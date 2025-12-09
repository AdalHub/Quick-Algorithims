import sqlite3

class Database:
    def __init__(self, file_name):
        connection = sqlite3.connect(file_name)
    
    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor
    def __exit__(self):
        self.cursor.commit()
        self.cursor.close()

def outter(): #example of a closure
    x= 10
    def inner():
        return x
    return inner()
func= outter()
print(func)

arr = []
for i in range(10):
    arr.append(i)
#demonstration of the use of lambda functions
new_arr= map(lambda x: x*10, arr)
print(list(new_arr))

import time
class Timer:
    def __init__(self):
        pass
    def __enter__(self):
        self.initial_time = time.time()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        elapsed= time.time()-self.initial_time
        print(elapsed)
        return False

# using context manager to time a block
with Timer():
    #doing something
    time.sleep(5)


a = "hello"
b = "hello"
print( a is b)
print( id(a) is id(b))
c= a
print(f"is a equal to c?:  {id(a) is id(c)}")
dic= {1:"a", 1.0: "b", True: "c"}
print(dic)

import time
def timer(func):
    def wrapper(*args):
        curTime =time.time()
        func(*args)
        print(f"function {func} took {time.time()-curTime}")
    return wrapper
@timer
def foo(n: int):
    time.sleep(n)
foo(3)
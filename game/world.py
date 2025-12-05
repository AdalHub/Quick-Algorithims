import time
def takeTime(func):
    def wrapper(*args):
        x =time.time()
        func(*args)
        print(f" this function took {time.time()-x} time")
    return wrapper
@takeTime
def funcToTest(n):
    time.sleep(n)
funcToTest(2)
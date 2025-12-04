import time
import threading

def foo():
    for _ in range(10):
        time.sleep(1)
        print("hello")


def bar():
    for _ in range(10):
        time.sleep(1)
        print("hi")
def main():
    t1 = threading.Thread(target = foo)
    t2 = threading.Thread(target = bar)
    t1.start()
    t2.start()
if __name__ == "__main__":
    main()
import time
import threading
import queue
def prodoucer(queue):
    for i in range(10):
        item = f"\\\ {i} ///" 
        queue.put(item)
        print(f"production of item {item}")
        time.sleep(1)
    queue.put(None)
def consumer(queue):
    while True:
        item= queue.get()
        if not item:
            break
        print(f"CONSUMING item: {item}")
        time.sleep(2)
def main():
    q = queue.Queue()
    t1 = threading.Thread(target = prodoucer, args=(q,))
    t2 = threading.Thread(target = consumer, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
if __name__ == "__main__":
    main()
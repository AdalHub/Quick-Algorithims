import time
import threading
import queue
from multiprocessing import Process



def cpu_bound_task(n):
    counter=0
    #we start a large counter in order to simulate a cpu intensive task
    for _ in range(n):
        counter+=1

def main():
    #no threading applied to cpu intensive task
    initial_time= time.time()
    for _ in range(4):
        cpu_bound_task(10**7)
    print(f"task took {time.time()-initial_time} WITH OUT threading" )

    #cpu intensive task with threading
    initial_time = time.time()
    threads= [threading.Thread(target= cpu_bound_task, args=(10**7,)) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"task took {time.time()-initial_time} with threading" )

    #cpu intensive task with multiprocessing
    initial_time = time.time()
    processes= [Process(target= cpu_bound_task, args=(10**7,)) for _ in range(4)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print(f"task took {time.time()-initial_time} with multi-processing" )
    print("as one may notice threading did not help in fact it might've made our program slower")
    print("but with multi-processing we are able to instantiate multiple interpreters and use more than 1 core")
if __name__ == "__main__":
    main()
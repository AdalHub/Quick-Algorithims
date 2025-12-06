import time
import threading
import queue
from multiprocessing import Process



def cpu_bound_task(n):
    counter=0
    #we start a large counter in order to simulate a cpu intensive task
    for _ in range(n):
        counter+=1

def main_cpu():
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



# now lets look at a case of threading vs multiprocessing for i/o bound tasks

import requests

def get_website(url):
    cur_time= time.time()
    response= requests.get(url, timeout=(5,10))#timeout set 5 to respond, 10 seconds to start reading
    #data = response.text
    print(f"url:{url}\n took {time.time()-cur_time} to respond")

    
def main_io():
    urls= ["https://www.google.com", "https://www.bing.com", "https://www.duckduckgo.com"]
    responce_times=[]
    #first lets measure the time using normal consecutive requests
    initial_time= time.time()
    for url in urls:
        get_website(url)
    responce_times.append(f"No concurrency: {time.time()-initial_time}")

    #now lets measure with threading
    threads= [threading.Thread(target= get_website, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    responce_times.append(f"Threading: {time.time()-initial_time}")

    #now lets measure with multiprocessing
    processes= [Process(target= get_website, args=(url,)) for url in urls]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    responce_times.append(f"Multiprocess time: {time.time()-initial_time}" )

    for res in responce_times:
        print(res)

if __name__ == "__main__":
    #main_cpu()
    main_io()

import requests
import asyncio
import time
import threading
from multiprocessing import Process
import aiohttp

def get_website(url):
    if not isinstance(url, str):
        return "invalid input"
    cur_time= time.time()
    requests.get(url, timeout=(5,10))#timeout set 5 to respond, 10 seconds to start reading
    
    print(f"url:{url}\n took {time.time()-cur_time} to respond")

async def get_website_async(url):
    if type(url) != str:
        return "invalid input"
    cur_time= time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            await response.text()  # Actually await the response
    
    return f"url:{url}\n took {time.time()-cur_time} to respond"

    
async def main_io():
    urls= ["https://www.google.com", "https://www.bing.com", "https://www.duckduckgo.com"]
    responce_times=[]
    #first lets measure the time using normal consecutive requests(synchronous)
    initial_time= time.time()
    for url in urls:
        get_website(url)
    responce_times.append(f"No concurrency: {time.time()-initial_time}")

    # threading
    initial_time = time.time()
    threads = [threading.Thread(target=get_website, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    responce_times.append(f"Threading: {time.time()-initial_time}")

    # multiprocessing
    initial_time = time.time()
    processes = [Process(target=get_website, args=(url,)) for url in urls]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    responce_times.append(f"Multiprocess time: {time.time()-initial_time}")

    # asyncio
    initial_time = time.time()
    tasks = [asyncio.create_task(get_website_async(url)) for url in urls]
    for t in tasks:
        await t
    responce_times.append(f"Asyncio time: {time.time()-initial_time}")

    print("\n=== Results ===")
    for res in responce_times:
        print(res)




if __name__ == "__main__":
    #main_cpu()
    asyncio.run(main_io())
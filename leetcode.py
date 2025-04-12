from collections import deque
# list has a pair as tuple of (a,b)
#list ((0,1)) take one before zero
#list has pair (2,3), take 3 before 2
#determines whether its possible to complete this course schedule 
#n amount of courses,

#set
dic={1: [2], 2: [3,4], 5:[6], 6: [5]}
def bfs(dic, key1):
    
    q= deque(key1)
    while q:
        curr= q.popleft()
        if curr in visited:
            return False
        visited.add(curr)

        for n in dic[curr]:
            q.append(n)
    return True
visited=set()
for n in dic:
    if n not in visited:
        if not bfs(dic, dic[n]):
            return False

#traverse graphs, bfs, dfs



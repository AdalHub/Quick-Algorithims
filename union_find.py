from collections import deque
#quick union
#  implementation
class NodeList:

    def __init__(self, arr):
        
        self.dic= {i:None for i in range(len(arr))}
        print(f"initializing dictionary {self.dic}")


        for i in range(len(arr)):
            self.dic[i] = arr[i]
        print(f"Filling in dictionary{self.dic}")


        self.adj = {i:[] for i in range(len(arr))}
        for n in range(len(arr)):
            if n != arr[n]:
                self.adj[n].append(arr[n])
                self.adj[arr[n]].append(n)
        print(f"making adjacency list {self.adj}")
        #implementation of a tracking of the size of each component using a queue to traverse each node once
        #recording the nodes that are part of one component using the cycle set
        #o(n) solution is achieved using a set to prevent visiting repeated nodes
        self.visit = set()
        self.sz= {i: 1 for i in range(len(arr))}
        print(f"initializing sz dictionary {self.sz}")

        def bfs(node):
            cycle = set()
            totSize =1
            q= deque([node])
            self.visit.add(node)
            cycle.add(node)
            while q:
                cur = q.popleft()
                for nei in self.adj[cur]:
                    if nei not in self.visit:
                        q.append(nei)
                        self.visit.add(nei)
                        cycle.add(nei)
                        totSize+=1
            for c in cycle:
                self.sz[c] = totSize

        for i in range(len(arr)):
            if i not in self.visit:
                bfs(i)
        print(f"finished setting sizes{self.sz}")


    def root(self,p):
        i=p
        cur = self.dic[i]
        while self.dic[i]!= i:
            print(f"analyzing index of {i} with root= {cur}")
            i= self.dic[i]
            cur = self.dic[i]
        if self.dic[i]== i:
            return i
        
    def union(self,p, q):
        i = self.root(p)
        j =self.root(q)
        #adding weighting functionality
        if self.sz[i] >= self.sz[j]:
            self.dic[i] = self.dic[j]
            self.sz[j] += self.sz[i]
        else:
            self.sz[i] += self.sz[j]
            self.dic[j] = self.dic[i]
        print(f"new list {self.dic}")

def main():
    array = [0,0,0,3,3,1]
    newList = NodeList(array)
    print(f"what is the root of 1? {newList.root(1)}")
    print(f"Update my list to union 1 and 4 {newList.union(1, 4)}")
    print(f"what is the root of 1 now?{newList.root(1)}")

if __name__ == "__main__":
    main()
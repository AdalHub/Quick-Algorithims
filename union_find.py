#quick union
#  implementation
class NodeList:
    dic = {}
    def __init__(self, arr):
        self.dic= {}
        for i in range(len(arr)):
            self.dic[i] = arr[i]
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
        self.dic[self.root(p)]= self.root(q)
        print(f"new list {self.dic}")

def main():
    array = [0,1,2,0,4,5,3]
    newList = NodeList(array)
    print(newList.root(6))
    print(newList.union(1, 6))

if __name__ == "__main__":
    main()
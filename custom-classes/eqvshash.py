class Player:
    def __init__(self, value: int):
        #value is an immutable type 
        self.level= value

    def __len__(self):
        return self.level

    def __add__(self, other):
        if isinstance(other, Player):
            return self.level + other.level
        raise Exception("invalid type bruh")

    def __str__(self):
        return f"{self.level}"

    def __repr__(self):
        return f"Player(level = {self.level})"

    def __lt__(self, other):
        if isinstance(other, Player):
            return self.level < other.level
        raise Exception("invalid type bruh")

    def __lte__(self, other):
        if isinstance(other, Player):
            return self.level <= other.level
        raise Exception("invalid type bruh")

    def __gt__(self, other):
        if isinstance(other, Player):
            return self.level > other.level
        raise Exception("invalid type bruh")
    
    def __gte__(self, other):
        if isinstance(other, Player):
            return self.level >= other.level
        raise Exception("invalid type bruh")
    
    #we implement the __eq__ so now our object is unhashable, aka we wouldnt be able to use this class object as keys in a dictionary
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.level == other.level
        raise Exception("invalid type bruh")
    
    #hash is based on the SAME ATTRIBUTES as used in __eq__, this is because equal objects must have equal hashes
    def __hash__(self):
        return hash(self.level)

    def __ne__(self, other):
        if isinstance(other, Player):
            return self.level != other.level
        raise Exception("invalid type bruh")
    
    def __mul__(self, other):
        if isinstance(other, Player):
            return self.level * other.level
        raise Exception("invalid type bruh")
    
    def __truediv__(self, other):
        if isinstance(other, Player):
            return self.level / other.level
        raise Exception("invalid type bruh")
    
    def __getitem__(self):
        return self.level


    

def testHashes():
    p1 = Player(10)
    p2 = Player(10)
    print(p1 == p2) # prints true
    print(hash(p1) == hash(p2)) #prints true
    try:
        dic= {p1: "first player"} #if we didnt implement the __hash__ we would not be able to use it as the key
        print(dic)
    except TypeError as e:
        print(f"invalid type: {e}")
def main():
    testHashes()

if __name__ == "__main__":
    main()
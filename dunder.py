class Player:
    def __init__(self, value):
        self.level= value

    def __len__(self):
        return self.level

    def __add__(self, other):
        if isinstance(other, Player):
            return self.level + other.level
        raise Exception("invalid type bruh")

    def __str__(self):
        return f"{self.level}"

    def __str__(self):
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
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.level == other.level
        raise Exception("invalid type bruh")
    
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



timmy= Player(10)
johnny= Player(5)
print(timmy)
print(len(timmy))
print(timmy + johnny)
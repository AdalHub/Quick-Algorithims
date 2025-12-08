class Gnome():
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return f"thy name is {self._name}"
    @name.getter
    def name(self):
        return f"thy name is the mighty {self._name}"
    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name= value
        raise TypeError("Invalid type bruh")
    @name.deleter
    def name(self):
        del self._name

garry = Gnome("garry")
print(garry.name)
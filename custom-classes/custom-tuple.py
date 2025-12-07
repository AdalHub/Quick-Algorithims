
#for this example we inherit directly from the tuple class to improve performance as it is written in C
class upperTuple(tuple):
    def __new__(cls, iterable):
        upper_iterable = (s.upper() for s in iterable)
        return super().__new__(cls,upper_iterable)
    

def testUpperTuple():

    x = upperTuple(["Hello", "from", "arkansas"])
    print(x)

#now lets see the use cases for __new__ in the singleton pattern
#the singleton pattern can allow us to ensure only one instance of that class exists
#useful for global configurations

class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance= super().__new__(cls, *args, **kwargs)
        return cls._instance

def singletonTest():
    
    x = Singleton()
    y = Singleton()
    print(x is y)


#now lets look at another example of the singleton pattern
#imagine you have an object that is incredibly expensive to initialize such as opening a database
class Client:
    #we create a dictionary as our cache
    _loaded={}
    _db_file= "mydb.txt"
    def __new__(cls, clientId):
        if (client:= cls._loaded.get(clientId)) is not None:
            print(f"client {clientId} already exists: {client}")
            return client
        client = super().__new__(cls)
        cls._loaded[clientId]= client
        client._init_from_file(clientId, cls._db_file)
        return client 
    
    def _init_from_file(self, clientId, file)-> None:
        print(f"reading client {clientId} data from file {file}")

def testClient():
    x= Client(1)
    y = Client(1)
    z= Client(2)

def main():
    testClient()


if __name__ == "__main__":
    main()
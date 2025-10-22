
# This exaple below demonstrates how python functions are used as objects   

def f1():
    print("you just ran f1")

def f2(myFunc):
    myFunc()

f2(f1)
#--------------------------------------------------------------------------

# below demonstrates how wrapper functions inside other functions can add extra functionality on top of the argument function

def f3(myFunc):
    #this is our wrapper function that will add extra functionality to whatever function is passed in
    def wrapper():
        print("Extra functionality 1")
        myFunc()
        print("Extra functionality 2")
    #and then we return this function with extra functionality
    return wrapper

def f4():
    print("this is the execution of argument function f4")

f3(f4) #this prints nothing as it returns our new function wrapper with the wrapper + f4 functionality
f3(f4)() #this on the other hand, executes the returned wrapper function

#--------------------------------------------------------------------------

#Now if we dont wish to pass the function directly as an argument and have to execute it, we can use a decorator

def f5(myFunc):
    print("this is the only thing that prints if the wrapper isnt executed")
    #this is our wrapper function that will add extra functionality to whatever function is passed in
    def wrapper():
        print("Extra functionality 3")
        myFunc()
        print("Extra functionality 4")
    #and then we return this function with extra functionality
    return wrapper

#this is a decorator with the @ at the front. we are basically saying 
#grab this function below and feed it as an argument to f5 anytime f6 is ran
@f5
def f6():
    print("this is the execution of argument function f6")
#here we run f6 and it immedietly is thrown into our decorator function and execute the returned wrapper
f6 #this wont execute the wrapper that is returned
f6() #this will execute the wrapper that is returned

#--------------------------------------------------------------------------

#in this example below we show a more realistic use of decorators

import time
#we create this function which is used to measure how many seconds a function takes to execute
def timer(myFunc):
    # we must set *args, **kwargs as parameters for our wrapper function in order to pass onto functionToTime its arguments
    def wrapper(*args, **kwargs):
        # we start our timer
        initial = time.time()
        # wrapper passes on the arguments to our function
        #we can also store the return of our function
        whatDoYouReturn = myFunc(*args, **kwargs)
        print(f"the total time to execute was {time.time()- initial} seconds")
        print(whatDoYouReturn)
    return wrapper

@timer
def functionToTime(n):
    secret= "This is the return of our function"
    time.sleep(n)
    return secret
#our functionToTime is called, it is passed on to the decorator, the wrapper accepts our functions arguments
# our wrapper is executed
functionToTime(3)

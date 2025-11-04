
# since we declare both of these variables as constants, they both become part of the string pool
# hence, it returns True 
a = "hello"
b= "hello"
print(a is b)

a = (1,2)
b= (1,2)
print(a is b)

a = (1, 2)
b = tuple([1, 2])
print(a is b)   # False

num = 7
#This will print false as we are dynamically allocating the memory for for each string so it is not checked from heap pool of string , if it already exisits or not
#since it would have to allocate the space in memory, AND check if it is also part of the pool, which would be very inefficient
a= str(num)
b= str(num)
print(a is b)

import sys
a = sys.intern("abcdefghijklmnopqrstuvwxyzn1234567890!@#$%^&*()-=_+")
b = "abcdefghijklmnopqrstuvwxyzn1234567890!@#$%^&*()-=_+"
print(a is b)
#string interning (or string pooling), what determines if a string is interned or not is if there are spaces within in the string. or in other words the string looks like a function name
a = "some string"
b = "some_string"
print(a is b) # returns false
#but
a = "some_string"
b = "some_string"
print(a is b) # returns True

x= [1,2,3]
y= [1,2,3]
print(x == y) # returns true as their values are the same
print(x is y) #but this returns false because in CPython their id(which is their mem location) is not equal, as they are two independent objects(do to the fact that arrays are immutable)
#but
x= [1,2,3]
y= x
print(x is y) #making y equal to a refference will make y into a refference of the same object even if its a mutable object

# in this example below since __default__ will be used and mutated twice
def add_two_list(x= []):
    x.append(2)
    return x
first= add_two_list()
print(first)
second= add_two_list()
print(second)

#but in this code we avoid referencing the same array stored in __default__ by assigning the default argument to None
def add_two_list(x= None):
    return [2] if not x else x.append(2) 
first= add_two_list()
print(first)
second= add_two_list()
print(second)
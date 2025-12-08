class A:
    __slots__=('x')
class B(A):
    pass
class C(A):
    pass
class D(B, C):
    pass
d = D()
# python uses the C3 linearization algorithim to establish the method resolution order
print(D.__mro__)
'''
     A
    / \
   B   C 
    \ /
     D
'''
#b is selected first as it reads from left to right

#LETS LOOK AT AN EXAMPLE OF INHERITANCE WITH SLOTS 
'''class X:
    __slots__=('x',)
class Y:
    __slots__=('y',)
class Z(X, Y):
    __slots__=('z')
'''
#this causes conflict due to conflicting slots

#The way to fix it, is to use a base

"""class Base:
    __slots__=()
class X(Base):
    __slots__=('x',)
class Y(Base):
    __slots__=('y',)
class Z(X, Y):
    __slots__=('z',)
c= Z()"""
#actually base doesnt work might be due to python version conflict
#if base doesnt work then use single inheritance 
class Base:
    __slots__=()
class X(Base):
    __slots__=('x',)
class Y(X):
    __slots__=('y',)
class Z(Y):
    __slots__=('z',)
c= Z()
#this works! just need  to make sure your inheritance is linear
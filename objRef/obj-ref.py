import sys
import ctypes

class A:
    def __init__(self, value):
        self.value = value

print("---- create object ----")
x = A(10)

print("x =", x)
print("x.value =", x.value)

# id(obj) in CPython is the memory address of the PyObject in the heap
print("\n[id / address info]")
print("id(x) =", id(x))
print("hex(id(x)) =", hex(id(x)))

# Let's confirm that x in our current local namespace refers to that same object
print("\n[namespace lookup]")
print("'x' in locals()? ->", "x" in locals())
print("locals()['x'] is x? ->", locals()["x"] is x)

# show the locals() dict keys (these are the *names* stored in the current frame)
print("\nlocals() keys ->", list(locals().keys()))
print(list(locals()))

# reference count:
# sys.getrefcount(obj) returns the refcount +1 because passing it into the function
# itself temporarily creates another reference
print("\n[reference counting]")
print("sys.getrefcount(x) =", sys.getrefcount(x))

# We can also peek at CPython's internal refcount directly using ctypes.
# WARNING: This is CPython-specific and kinda sharp, but educational.
pyobj_addr = id(x)
pyobj_refcnt = ctypes.c_long.from_address(pyobj_addr).value
print("CPython internal refcount (approx) =", pyobj_refcnt)

# Let's create another reference y pointing to the SAME heap object
print("\n---- alias y = x ----")
y = x

print("y =", y)
print("y is x? ->", y is x)

print("\nafter y = x:")
print("sys.getrefcount(x) =", sys.getrefcount(x))
pyobj_refcnt2 = ctypes.c_long.from_address(id(x)).value
print("internal refcount now =", pyobj_refcnt2)

# Modify through y and see x change (because same object)
print("\n---- mutate through y ----")
y.value = 999
print("x.value =", x.value)
print("y.value =", y.value)

# Show that attributes are also objects with their own addresses
print("\n[id of attribute objects]")
print("x.value =", x.value)
print("id(x.value) =", id(x.value), "hex:", hex(id(x.value)))

# We can inspect that integer object's refcount too
int_refcnt = ctypes.c_long.from_address(id(x.value)).value
print("refcount of integer 999 =", int_refcnt)

print("\nDone.")

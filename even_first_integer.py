x = 11111221111
arr= list(str(x))
for i in range(len(arr)):
    arr[i] = int(arr[i])
print(arr)
def shiftEven(A):
    firstEven, firstOdd= 0, len(A)-1
    while firstEven <firstOdd:
        if A[firstEven] % 2==0:
            firstEven+=1
        else:
            A[firstEven], A[firstOdd] = A[firstOdd],A[firstEven]
            firstOdd-=1
    return A
print(shiftEven(arr))
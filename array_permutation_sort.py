
test= [2,0,1,3, 6,7,8,4,5]
#mySort function takes in an array of integers in any permutation order of [0,n-1] and sorts it 
def mySort(arr):
    def mySwitch(x,y):
        temp = arr[y]
        arr[y]= arr[x]
        arr[x]= temp
        if x != arr[x]:
            mySwitch(x, arr[x])

    for i in range(len(arr)):
        if arr[i] == i:
            continue
        mySwitch(i, arr[i])
    return arr
print(mySort(test))

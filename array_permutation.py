
test= [2,0,1,3, 6,7,8,4,5]

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

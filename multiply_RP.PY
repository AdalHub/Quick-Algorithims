def multiplyRP(num1,num2):
    num1, num2 = list(str(num1)), list(str(num2))
    for i in range(len(num1)):
        num1[i] = int(num1[i])
    for i in range(len(num2)):
        num2[i] = int(num2[i])
    sign = -1 if num1[0] ^ num2[0] else 1
    result = [0] * (len(num1)+ len(num2))

    for i in reversed(range(len(num1))):
        for j in reversed(range(len(num2))):
            result[i+j+1] += num1[i]*num2[j]
            result[i+j]+= result[i+j+1] //10
            result[i+j+1] %=10
    
    result= result[next((i for i, x in enumerate(result) if x!= 0),len(result)):] or [0]
    return [sign* result[0]] + result[1:]

print(multiplyRP(12345, 678))
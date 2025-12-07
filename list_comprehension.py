nested = [[1,2],[3,4],[5,6],[7,8]]
flat= [item for sublist in nested for item in sublist]
print(flat)
cartesian = [(x,y) for x in range(3) for y in 'abc']
print(cartesian)
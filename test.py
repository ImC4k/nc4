import numpy as np

# masked 2d array
a  = np.ma.array([[1, 2, 3], [4, 5, 6]], mask=[[0, 1, 0], [1, 0, 1]])
print(a)
print(a.shape)

a = np.transpose(a)
print(a)
print(a.shape)

print(a[0:3, 0:1])
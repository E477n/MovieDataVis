import numpy as np

testmatrix = [
    [1, 1/2, 4, 3, 3],
    [2, 1, 7, 5, 5],
    [1/4, 1/7, 1, 1/2, 1/3],
    [1/3, 1/5, 2, 1, 1],
    [1/3, 1/5, 3, 1, 1]
]
matrix1 = [
    [1, 1/3, 1/5, 1/7, 1/5],
    [3, 1, 1/3, 1/5, 1/3],
    [5, 3, 1, 1/3, 1],
    [7, 5, 3, 1, 3],
    [5, 3, 1, 1/3, 1]
]
matrix2 = [
    [1, 1/3, 1/5, 1/9, 1/5],
    [3, 1, 1/2, 1/3, 1/2],
    [5, 2, 1, 1/4, 1],
    [9, 3, 4, 1, 4],
    [5, 2, 1, 1/4, 1]
]

## condition2: without franchise, 4 factors
matrix3 = [
    [1, 1 / 3, 1 / 5, 1 / 5],
    [3, 1, 1 / 3, 1 / 3],
    [5, 3, 1, 1],
    [5, 3, 1, 1]
]
## condition3: without budget, 4 factors
matrix4 = [
    [1, 1/3, 1/5, 1/7],
    [3, 1, 1/3, 1/5],
    [5, 3, 1, 1/3],
    [7, 5, 3, 1],
]
## condition3: without budget, 4 factors
matrix5 = [
    [1, 1/3, 1/5],
    [3, 1, 1/3],
    [5, 3, 1],
]

def calculateWeightVector(matrix):
    a, b = np.linalg.eig(np.array(matrix))
    print("value:", a)

    # normalize vector
    sum = 0
    wb = []
    for i in b:
        sum += i[0]
    for i in b:
        wb.append(i[0] / sum)
    return wb

if __name__ == "__main__":
    print(calculateWeightVector(matrix5))
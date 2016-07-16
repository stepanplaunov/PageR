import numpy as np
import time

prograph = open('probability graph.txt')
starttime = time.time()


class Graph:
    def __init__(self, matrix):
        self.lists = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    self.lists.append([j, matrix[i][j]])


class Vector:
    def __init__(self, coordinats):
        self.coordinats = coordinats
        self.measurement = len(coordinats)

    def __add__(self, other):
        result = [0 for i in range(self.measurement)]
        for i in range(self.measurement):
            result[i] = self.coordinats[i] + other.coordinats[i]
        return Vector(result)

    def __sub__(self, other):
        result = [0 for i in range(self.measurement)]
        for i in range(self.measurement):
            result[i] = self.coordinats[i] - other.coordinats[i]
        return Vector(result)

    def __mul__(self, other):                                             #other = list of adjacents, other2 = list of adjacents with mass
        if type(other) == Vector:                                         #scalar mul
            result = 0
            for i in range(self.measurement):
                result += self.coordinats[i] * other.coordinats[i]
            return result
        elif type(other) == Graph:                                        #return Vector
            result = [0 for i in range(self.measurement)]
            for i in range(len(other.lists)):
                for j in range(len(other.lists[i])):
                    result[other.lists[i][j][0]] += self.coordinats[other.lists[i][j][0]] * other.lists[i][j][1]
        else:
            result = Vector([0 for i in range(self.measurement)])
            for i in range(self.measurement):
                result[i] = self.coordinats[i] * other
            return Vector(result)

    def __abs__(self):
        result = 0
        for i in range(self.measurement):
            result += self.coordinats[i] ** 2
        return result

    def norma(self):
        return abs(self) ** 2


def read(graph): #matrix reading
    global n
    n = int(graph.readline()) #n - length
    data = [[] for i in range(n)]
    for i in range(n):
        data[i] = list(map(float, graph.readline().split()))
        data[i][i] -= 1
    data = np.array(data)
    data = data.T
    ones = np.array([1] * n)
    data = np.row_stack((data, ones))
    return data

def norma(vector): #2-norma
    return sum(vector[i] ** 2 for i in range(n)) ** 0.5

def f(x): #f(x) - permanent function
    return 0.5 * norma(np.dot(A, x)) ** 2

def grad(x): #return gradient of f(x) = 0.5 * norma(A * x) ** 2
    return np.dot(A.T, np.dot(A, x) - b)

def f_(xnew, x, L, gradi): #f(x) - inspection function
    return f(x) + np.dot(gradi, xnew - x) + (L * norma(xnew - x) ** 2 / 2)

def main():
    global A, n, x, b
    A = read(prograph)                    #probability graph (matrix)
    b = np.array([0] * (n + 1))
    b[-1] = 1
    x = np.array([0] * n)                 #PageRank vector
    x[0] = 1.0
    EPS = 10 ** (-5)                      #accuracy
    L = 1
    gradi = grad(x)
    xnew = x - grad(x) / L
    while norma(grad(x) / L) > EPS:
        while f_(xnew, x, L, gradi) < f(xnew):
            L *= 2
            xnew = x - gradi / L
        x = xnew
        gradi = grad(x)
        xnew = x - gradi / L
        L /= 2
    print(*x)
    print(sum(x))
    print(time.time() - starttime)

main()

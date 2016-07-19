import numpy as np
import time
from scipy.sparse import csr_matrix

starttime = time.time()
prograph = open('probability graph.txt')

def read(graph):  # matrix reading
    global n
    n = int(graph.readline())  # n - length
    data = [[] for i in range(n)]
    for i in range(n):
        data[i] = list(map(float, graph.readline().split()))
        data[i][i] -= 1
    data = np.array(data)
    data = data.T
    data = csr_matrix(data)
    return data

def norma(vector):  # 2-norma
    return np.linalg.norm(vector, 2)

def f(x):  # f(x) - permanent function
    return 0.5 * norma(A.dot(x) - b) ** 2

def grad(x):  # return gradient of f(x) = 0.5 * norma(A * x) ** 2
    return A.T.dot(A.dot(x) - b)

def f_(xnew, x, L, gradx):  # f(x) - inspection function
    return f(x) + np.dot(gradx, xnew - x) + (L * norma(xnew - x) ** 2 / 2)

def main():
    global A, n, x, b
    A = read(prograph)  # probability graph (matrix)
    prograph.close()
    b = np.array([0.0] * (n))
    x = np.array([0.0] * n)  # PageRank vector
    x[0] = 1.0
    EPS = 10 ** (-3)  # accuracy
    #L = 10
    #gradx = grad(x)
    #xnew = x - gradx / L
    firstage = time.time()
    print(b)
    print(A.dot(x))
    print(x)
    print('---')
    r = b - A.dot(x)
    z = r

    while f(x) > EPS:
        r_2 = np.dot(r, r)
        alpha = r_2 / np.dot(A.dot(z), z)
        x = x + alpha * z
        r = r - alpha * A.dot(z)
        beta = np.dot(r, r) / r_2
        z = r + beta * z
    print(f(x))
    x = x / x.sum()
    print(time.time() - firstage)

'''
    while f(x) > EPS:
        while f_(xnew, x, L, gradx) <= f(xnew):
            L *= 2
            xnew = x - gradx / L
        #print(L, f(x))
        x = xnew
        gradx = grad(x)
        L /= 2
        xnew = x - grad(x) / L
'''

main()

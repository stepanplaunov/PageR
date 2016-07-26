#Fast Gradient method

import numpy as np

def read(graph):
    n = graph.shape[0]
    for i in range(n):
        graph[i, i] -= 1
    graph = graph.transpose()
    graph.resize((n + 1, n))
    for i in range(n):
        graph[-1, i] = 1.0 / n
    return graph.tocoo().tocsr(), n

def norma(vector):
    return np.linalg.norm(vector, 2)

def f(A, x, b):
    return 0.5 * norma(A.dot(x) - b) ** 2

def grad(A, x, b):
    return A.T.dot(A.dot(x) - b)

def f_(xnew, x, L, gradi, A, b):
    return f(A, x, b) + np.dot(gradi, xnew - x) + (L * norma(xnew - x) ** 2 / 2)

def fgm(graph):
    A, n = read(graph)
    k = 0
    b = np.array([0] * (n + 1))
    b[-1] = 1.0
    b = b / n
    x = np.array([0] * n)
    x[0] = 1.0
    EPS = 10 ** (-3)
    L = 10
    y = x.copy()
    z = x.copy()
    ynew = (2 * z + k * x) / (k + 2)
    grady = grad(A, ynew, b)
    xnew = ynew - grady / L
    znew = z - (k + 2) * grady / (2 * L)
    k += 1
    while f(A, x, b) > EPS:
        while f_(xnew, ynew, L, grady, A, b) < f(A, xnew, b):
            L *= 2
            grady = grad(A, ynew, b)
            xnew = ynew - grady / L
            znew = z - (k + 2) * grady / (2 * L)
        x, y, z = xnew, ynew, znew
        grady = grad(A, ynew, b)
        L /= 2
        k += 1
        ynew = (2 * z + k * x) / (k + 2)
        xnew = ynew - grady / L
        znew = z - (k + 2) * grady / (2 * L)
    x = x / x.sum()
    return x

import numpy

def norm(vector):
    return sum(vector[i] ** 2 for i in range(vector.size)) ** 0.5

def f(x):
    return x ** 2

def f_(x, xold, L): # x, xold - Vector
    return (f(xold) + numpy.gradient(f(xold)) * (x - xold) + L / 2 * numpy.linalg.norm(x - xold, 2))

def main():
    x = numpy.array([1, 2, 1, 2])
    L = 1
    EPS = 10 ** (-4)
    function = 'y = x ** 2 + 2 * x + 1'
    f_gradient = numpy.gradient(f(x))
    while numpy.linalg.norm(f_gradient, 2) > EPS:
        xold = x
        x = x - 1 / L * f_gradient
        print(f_(x, xold, L))
        while f_(x, xold, L) < f(x):
            L *= 2
            x = x - 1/L * f_gradient
        print(x, xold)
        L /= 2
        f_gradient = numpy.gradient(f(x))
    print(x, f(x))

main()

from random import randint as rnd
import time

matrix = open('probability graph.txt', 'w')
#data = open("inbox_data", "w")

V = 50000
K = 10
a = 10000

def rand(n):
    f = rnd(1, (a + 1) * n)
    if f == 1:
        return(n)
    elif f <= a:
        return(rnd(0, n - 1))
    else:
        return(vertexs[rnd(0, len(vertexs) - 1)])

def edge(j, i):
    vertexs.append(j)
    vertexs.append(i)
    graph[i // K][j // K] += 1
    #inbox[i // K].append(j // K)
    if j // K != i // K:
        graph[j // K][i // K] += 1
        #inbox[j // K].append(i // K)
    numbers[i // K] += 1
    numbers[j // K] += 1


def for_print():
    matrix.write(str(V // K))
    matrix.write("\n")
    #data.write(str(V // K))
    #data.write("\n")
    for i in range(V // K):
        matrix.write(" ".join(map(str, graph[i])))
        matrix.write("\n")
        #data.write(" ".join(map(str, inbox[i])))
        #data.write("\n")

def division():
    for i in range(V // K):
        for j in range(V // K):
            graph[i][j] /= numbers[i]

def main():
    global vertexs, graph, numbers, inbox
    starttime = time.time()
    graph = [[0] * (V // K) for i in range(V // K)]
    numbers = [0] * (V // K)
    graph[0][0] = 1
    vertexs = [0]
    #inbox = [[] for i in range(V // K)]
    for i in range(1, V):
        j = rand(i)
        edge(j, i)
    division()
    for_print()
    print(time.time() - starttime)

main()

from random import randint as rnd
matrix = open('probability graph.txt', 'w')

V = 1000

def rand(i):
    if rnd(1, (i + 1) * 2 - 1) == 1:
        return(i)
    else:
        return(vertexs[rnd(0, i * 2 - 2)])

def edge(j, i):
    graph[i][j] = 1
    graph[j][i] = 1
    vertexs.append(j)
    vertexs.append(i)

def for_print(graph):
    matrix.write(str(V))
    matrix.write("\n")

    for i in range(V):
        matrix.write(" ".join(map(str, graph[i])))
        matrix.write("\n")

def main():
    global graph, vertexs
    graph = [[0] * V for i in range(V)]
    graph[0][0] = 1
    vertexs = [0]
    for i in range(1, V):
        j = rand(i)
        edge(j, i)
    for_print(graph)

main()
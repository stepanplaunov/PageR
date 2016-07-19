LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
import random
import geometry
radius = 500
points = []
segments = []
reader = open('probability graph.txt', 'r')
n = int(reader.readline())
data = []
for i in range(n):
    data.append(list(map(float, reader.readline().split())))


points = [[] for i in range(n)]
for i in range(n):
    x = 2 * radius * (i - n // 2 + 0.5) / n
    points[i] = [geometry.Point(x, (radius ** 2 - x ** 2) ** 0.5 - radius // 3), str(i)]
for i in range(n):
    for j in range(i, n):
        if data[i][j] != 0:
            segments.append([geometry.Segment(points[i][0], points[j][0]), points[i][1] + points[j][1]])

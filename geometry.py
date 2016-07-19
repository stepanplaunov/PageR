import math


class Point:
    def __init__(self, first, second):
        if ((type(first) == int or type(first) == float) and
                (type(second) == int or type(second) == float)):
            self.x = first
            self.y = second

    def __str__(self):
        return ('Point' + ' ' + str(self.x) + ' ' + str(self.y))

    def __neg__(self):
        return (Point(-self.x, -self.y))

    def __eq__(self, other):
        if type(other) == Point:
            return (self.x - other.x == 0 and
                    self.y - other.y == 0)

    def __add__(self, other):
        if type(other) == Vector:
            return (Point(self.x + other.x,
                          self.y + other.y))

    def __sub__(self, other):
        if type(other) == Vector:
            return (Point(self.x - other.x,
                          self.y - other.y))

    def __rshift__(self, other):
        if type(other) == Point:
            return (((self.x - other.x) ** 2 +
                     (self.y - other.y) ** 2) ** 0.5)
        if type(other) == Line:
            return (abs((other.A * self.x + other.B * self.y + other.C) /
                        (other.A ** 2 + other.B ** 2) ** 0.5))
        if type(other) == Segment:
            if (Vector(other.A, self) ** Vector(other.A, other.B) > 0 and
                            Vector(other.B, self) ** Vector(other.B, other.A) > 0):
                return (self >> Line(other.A, other.B))
            else:
                return (min(self >> other.A,
                            self >> other.B))


class Vector:
    def __init__(self, first, second):
        if ((type(first) == int or type(first) == float) and
                (type(second) == int or type(second) == float)):
            self.x = first
            self.y = second
        if type(first) == Point and type(second) == Point:
            self.x = second.x - first.x
            self.y = second.y - first.y

    def __str__(self):
        return ('Vector' + ' ' + str(self.x) + ' ' + str(self.y))

    def __abs__(self):
        return ((self.x ** 2 + self.y ** 2) ** 0.5)

    def __eq__(self, other):
        if type(other) == Vector:
            return (self.x - other.x == 0 and
                    self.y - other.y == 0)

    def __add__(self, other):
        if type(other) == Vector:
            return (Vector(self.x + other.x,
                           self.y + other.y))

    def __sub__(self, other):
        if type(other) == Vector:
            return (Vector(self.x - other.x,
                           self.y - other.y))

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return (Vector(self.x * other,
                           self.y * other))
        if type(other) == Vector:
            return (self.x * other.y -
                    self.y * other.x)

    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            return (Vector(self.x / other,
                           self.y / other))

    def __pow__(self, other):
        if type(other) == Vector:
            return (self.x * other.x +
                    self.y * other.y)

    def __floordiv__(self, other):
        if type(other) == int or type(other) == float:
            return (Vector(self.x // other,
                           self.y // other))

    def unit_vector(self):
        return (self / abs(self))


class Line:
    def __init__(self, first, second, third=None):
        if third == None:
            self.A = first.y - second.y
            self.B = second.x - first.x
            self.C = first.x * second.y - first.y * second.x
            self.first = first
            self.second = second
        if third != None:
            self.A = first
            self.B = second
            self.C = third
            self.first = Point(-(first * third) / (first ** 2 + second ** 2),
                               -(second * third) / (first ** 2 + second ** 2))
            self.second = self.first + Vector(-second, first)

    def __str__(self):
        return ('Line' + ' ' + str(self.A) + ' ' + str(self.B) + ' ' + str(self.C))

    def __eq__(self, other):
        if type(other) == Line:
            return (self.A - other.A == 0 and
                    self.B - other.B == 0 and
                    self.C - other.C == 0)

    def __rshift__(self, other):
        if type(other) == Point:
            return (abs((self.A * other.x + self.B * other.y + self.C) /
                        (self.A ** 2 + self.B ** 2) ** 0.5))
        if type(other) == Line:
            if Line & Line == None:
                return (self.first >> other)
            if Line & Line != None:
                return (0)

    def __contains__(self, other):
        if type(other) == Point:
            return ((other >> self) == 0)

    def __and__(self, other):
        if type(other) == Line:
            if self.A * other.B != self.B * other.A:
                return (Point((self.B * other.C - self.C * other.B) / (self.A * other.B - self.B * other.A),
                              (self.C * other.A - self.A * other.C) / (self.A * other.B - self.B * other.A)))
            if (self.A * other.B == self.B * other.A and
                            self.A * other.C == self.C * other.A):
                return (self)
            if (self.A * other.B == self.B * other.A and
                            self.A * other.C != self.C * other.A):
                return ()
        if type(other) == Circle:
            if (other.O >> self) == other.radius:
                return (self & self.perpendicular_line(other.O))
            if (other.O >> self) < other.radius:
                return ((self & self.perpendicular_line(other.O)) +
                        Vector(self.first, self.second).unit_vector() *
                        (other.radius ** 2 - (other.O >> self) ** 2) ** 0.5,
                        (self.perpendicular_line(other.O) & self) -
                        Vector(self.first, self.second).unit_vector() *
                        (other.radius ** 2 - (other.O >> self) ** 2) ** 0.5)
            if (other.O >> self) > other.radius:
                return ()

    def parallel_line(self, other):
        if type(other) == int or type(other) == float:
            return (Line(self.A,
                         self.B,
                         self.C - other * (self.A ** 2 + self.B ** 2) ** 0.5))
        if type(other) == Point:
            return (Line(other,
                         other + Vector(-self.B, self.A)))

    def perpendicular_line(self, other):
        if type(other) == Point:
            return (Line(-self.B,
                         self.A,
                         self.B * other.x - self.A * other.y))


class Circle:
    def __init__(self, first, second, third=None):
        if third == None:
            self.O = first
            self.radius = second
        if third != None:
            self.O = Triangle(first, second, third).circumscribed_circle().O
            self.radius = Triangle(first, second, third).circumscribed_circle().radius

    def __str__(self):
        return ('Circle' + ' ' + str(self.O) + ' ' + str(self.radius))

    def __eq__(self, other):
        if type(other) == Circle:
            return (self.radius - other.radius == 0)

    def __contains__(self, other):
        if type(other) == Point:
            return ((self.O >> other) == self.radius)

    def __and__(self, other):
        if type(other) == Line:
            if (self.O >> other) == self.radius:
                return (other & other.perpendicular_line(self.O))
            if (self.O >> other) < self.radius:
                return ((other & other.perpendicular_line(self.O)) +
                        Vector(other.first, other.second).unit_vector() *
                        (self.radius ** 2 - (self.O >> other) ** 2) ** 0.5,
                        (other & other.perpendicular_line(self.O)) -
                        Vector(other.first, other.second).unit_vector() *
                        (self.radius ** 2 - (self.O >> other) ** 2) ** 0.5)
            if (self.O >> other) > self.radius:
                return ()
        if type(other) == Circle:
            if self.O == other.O:
                if self.radius == other.radius:
                    return (self)
                if self.radius != other.radius:
                    return ()
            if self.O != other.O:
                if self.radius + other.radius == (self.O >> other.O):
                    return (self.O + Vector(self.O, other.O).unit_vector() * self.radius)
                if self.radius + other.radius > (self.O >> other.O):
                    return (self & Line(self.O, other.O).perpendicular_line(self.O +
                                                                            Vector(self.O, other.O).unit_vector() *
                                                                            ((
                                                                             self.O >> other.O) ** 2 + self.radius ** 2 - other.radius ** 2) /
                                                                            ((self.O >> other.O) * 2)))
                if self.radius + other.radius < (self.O >> other.O):
                    return ()

    def perimeter(self):
        return (self.radius * math.pi * 2)

    def area(self):
        return (self.radius ** 2 * math.pi)

    def tangent_line(self, other):
        if type(other) == Point:
            if other in self:
                return (Line(self.O, other).perpendicular_line(other))
            if other not in self:
                if self.radius < (self.O >> other):
                    return (Line(other, (self & Circle(other, ((self.O >> other) ** 2 - self.radius ** 2) ** 0.5))[0]),
                            Line(other, (self & Circle(other, ((self.O >> other) ** 2 - self.radius ** 2) ** 0.5))[1]))
                if self.radius > (self.O >> other):
                    return ()


class Segment:
    def __init__(self, first, second):
        if type(first) == Point and type(second) == Point:
            self.A = first
            self.B = second

    def __str__(self):
        return ('Segment' + ' ' + str(self.A) + ' ' + str(self.B))

    def __abs__(self):
        return (self.A >> self.B)

    def __eq__(self, other):
        if type(other) == Segment:
            return (abs(self) - abs(other) == 0)

    def __add__(self, other):
        if type(other) == Vector:
            return (Segment(self.A + other,
                            self.B + other))

    def __sub__(self, other):
        if type(other) == Vector:
            return (Segment(self.A - other,
                            self.B - other))

    def __rshift__(self, other):
        if type(other) == Point:
            if (Vector(self.A, other) ** Vector(self.A, self.B) > 0 and
                            Vector(self.B, other) ** Vector(self.B, self.A) > 0):
                return (other >> Line(self.A, self.B))
            if (Vector(self.A, other) ** Vector(self.A, self.B) <= 0 or
                            Vector(self.B, other) ** Vector(self.B, self.A) <= 0):
                return (min(other >> self.A,
                            other >> self.B))

    def __contains__(self, other):
        if type(other) == Point:
            return ((other >> self) == 0)

    def proportion(self, other):
        if type(other) == int or type(other) == float:
            return (self.A + Vector(self.A, self.B) * other)


class Beam:
    def __init__(self, first, second):
        if type(second) == Point:
            self.O = first
            self.direct = Vector(first, second)
        if type(second) == Vector:
            self.O = first
            self.direct = second

    def __eq__(self, other):
        if type(other) == Beam:
            return (self.O == other.O and
                    self.direct == other.direct)

    def __str__(self):
        return ('Beam' + ' ' + str(self.O) + ' ' + str(self.direct))

    def __rshift__(self, other):
        if type(other) == Point:
            if Vector(self.O, other) ** self.direct > 0:
                return (other >> Line(self.O, self.O + self.direct))
            if Vector(self.O, other) ** self.direct <= 0:
                return (other >> self.O)

    def __contains__(self, other):
        if type(other) == Point:
            return (other >> self == 0)


class Angle:
    def __init__(self, first, second, third=None):
        if third == None:
            if type(first) == Beam and type(second) == Beam:
                self.first = first.direct
                self.second = second.direct
                self.O = first.O
                self.A = first.O + first.direct
                self.B = second.O + second.direct
        if third != None:
            if type(first) == Point and type(second) == Point and type(third) == Point:
                self.first = Vector(second, first)
                self.second = Vector(second, third)
                self.O = second
                self.A = first
                self.B = third
            if type(first) == Point and type(second) == Vector and type(third) == Vector:
                self.first = second
                self.second = third
                self.O = first
                self.A = first + second
                self.B = first + third

    def __str__(self):
        return ('Angle' + ' ' + str(self.O) + ' ' + str(self.first) + ' ' + str(self.second))

    def __abs__(self):
        return (math.acos(self.first ** other.first / (abs(self.first) * abs(self.second))))

    def __eq__(self, other):
        if type(other) == Angle:
            return (abs(self) - abs(other) == 0)

    def __contains__(self, other):
        return (((Triangle(self.A, other, self.O).oriented_area() <= 0 and Triangle(self.A, self.B,
                                                                                    self.O).oriented_area() <= 0) and
                 (Triangle(self.B, other, self.O).oriented_area() >= 0 and Triangle(self.B, self.A,
                                                                                    self.O).oriented_area() >= 0)) or
                ((Triangle(self.A, other, self.O).oriented_area() >= 0 and Triangle(self.A, self.B,
                                                                                    self.O).oriented_area() >= 0) and
                 (Triangle(self.B, other, self.O).oriented_area() <= 0 and Triangle(self.B, self.A,
                                                                                    self.O).oriented_area() <= 0)))


class Triangle:
    def __init__(self, first, second, third):
        if type(first) == Point and type(second) == Point and type(third) == Point:
            self.A = first
            self.B = second
            self.C = third
            self.AB = Segment(first, second)
            self.BC = Segment(second, third)
            self.AC = Segment(first, third)
            self.ABC = Angle(first, second, third)
            self.ACB = Angle(first, third, second)
            self.BAC = Angle(second, first, third)

    def __str__(self):
        return ('Triangle' + ' ' + str(self.A) + ' ' + str(self.B) + ' ' + str(self.C))

    def __eq__(self, other):
        if type(other) == Triangle:
            return ({self.AB, self.BC, self.AC} ==
                    {other.AB, other.BC, other.AC})

    def __add__(self, other):
        if type(other) == Vector:
            return (Triangle(self.A + other,
                             self.B + other,
                             self.C + other))

    def __sub__(self, other):
        if type(other) == Vector:
            return (Triangle(self.A - other,
                             self.B - other,
                             self.C - other))

    def perimeter(self):
        return (self.AB + self.BC + self.AC)

    def area(self):
        return (abs(Vector(self.B.x - self.A.x,
                           self.B.y - self.A.y) *
                    Vector(self.C.x - self.A.x,
                           self.C.y - self.A.y)) / 2)

    def oriented_area(self):
        return (Vector(self.B.x - self.A.x,
                       self.B.y - self.A.y) *
                Vector(self.C.x - self.A.x,
                       self.C.y - self.A.y) / 2)

    def centroid(self):
        return (Point((self.A.x + self.B.x + self.C.x) / 3,
                      (self.A.y + self.B.y + self.C.y) / 3))

    def incenter(self):
        return (Point((self.A.x * self.BC + self.B.x * self.AC + self.C.x + self.AB) / self.perimeter(),
                      (self.A.y * self.BC + self.B.y * self.AC + self.C.y + self.AB) / self.perimeter()))

    def orthocenter(self):
        return (Line(self.A, self.B).perpendicular_line(self.C) &
                Line(self.A, self.C).perpendicular_line(self.B))

    def circumcenter(self):
        return (Line(self.A, self.B).perpendicular_line(Point((self.A.x + self.B.x) / 2,
                                                              (self.A.y + self.B.y) / 2)) &
                Line(self.A, self.C).perpendicular_line(Point((self.A.x + self.C.x) / 2,
                                                              (self.A.y + self.C.y) / 2)))

    def inscribed_circle(self):
        return (Circle(self.incenter(), self.A >> self.incenter()))

    def circumscribed_circle(self):
        return (Circle(self.circumcenter(), self.A >> self.circumcenter()))

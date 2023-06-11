import math
from matplotlib import pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not (self == other)
    
    def __hash__(self):
        return hash((self.x,self.y))
    
    def distance_to(self, point2):
        return math.sqrt((self.x-point2.x)**2 + (self.y-point2.y)**2)

class Line:
    def __init__(self, a, b, c):
        # line is defined as ax+by+c
        self.a = a
        self.b = b
        self.c = c

    def find_perpendicular(self, p : Point):
        # finds a Line perpendicular to itself through point p
        if self.b == 0:
            return Line(0,1,-p.y)
        if self.a == 0:
            return Line(1,0,-p.x)
        a2 = self.b
        b2 = -self.a
        c2 = -a2*p.x - b2*p.y
        return Line(a2,b2,c2)
    
    def find_intersection(self, line2):
        if self.a == 0 and line2.a == 0:
            return None
        if self.a != 0 and line2.a != 0 and self.b/self.a == line2.b/line2.a:
            return None
        
        x = (self.b*line2.c-self.c*line2.b)/(self.a*line2.b-self.b*line2.a)
        y = (self.c*line2.a-self.a*line2.c)/(self.a*line2.b-self.b*line2.a)
        return Point(x, y)
    
    def same_side(self, point1, point2):
        if (self.a*point1.x+self.b*point1.y+self.c) * (self.a*point2.x + self.b*point2.y + self.c) > 0:
            return True
        return False

class Edge:
    def __init__(self, point1 : Point, point2 : Point):
        # switching point1 and point2 should result in the same edge for hashing purposes
        if point1.x > point2.x or (point1.x == point2.x and point1.y > point2.y):
            self.point1 = point2
            self.point2 = point1
        else:
            self.point1 = point1
            self.point2 = point2

    def __eq__(self, other):
        return (self.point1 == other.point1 and self.point2 == other.point2) or (self.point1 == other.point2 and self.point2 == other.point1)
    
    def __ne__(self, other):
        return not (self == other)
    
    def __hash__(self):
        return hash((self.point1, self.point2))

    def get_line(self):
        if self.point1.x == self.point2.x:
            return Line(1,0,-self.point1.x)
        if self.point1.y == self.point2.y:
            return Line(0,1,-self.point2.y)
        a = (self.point2.y - self.point1.y)/(self.point1.x-self.point2.x)
        b = 1
        c = -b*self.point1.y - a*self.point1.x
        return Line(a,b,c)
    
    def get_midpoint(self):
        return Point((self.point1.x+self.point2.x)/2, (self.point1.y+self.point2.y)/2)

class Triangle:
    def __init__(self, point1 : Point, point2 : Point, point3 : Point):
        self.points = [point1, point2, point3]
        self.edges = [Edge(self.points[0], self.points[1]),Edge(self.points[0], self.points[2]),Edge(self.points[1], self.points[2])]
        self.circumcenter, self.circumradius = self.find_circumcircle()

    def __eq__(self, other):
        return self.points == other.points

    def find_circumcircle(self):
        # only need to use two edges as perpendiculars to them intersect at the same point
        line1 = self.edges[0].get_line()
        line2 = self.edges[1].get_line()

        midpoint1 = self.edges[0].get_midpoint()
        midpoint2 = self.edges[1].get_midpoint()

        perp1 = line1.find_perpendicular(midpoint1)
        perp2 = line2.find_perpendicular(midpoint2)

        c = perp1.find_intersection(perp2)
        r = c.distance_to(self.points[0])
        return (c,r)
    
    def point_in_circumcircle(self, p : Point):
        if self.circumcenter.distance_to(p) <= self.circumradius:
            return True
        return False
    
    def plot_triangle(self, ax, with_circle=False):
        for edge in self.edges:
            ax.plot([edge.point1.x,edge.point2.x],[edge.point1.y,edge.point2.y],color="black")
        if with_circle:
            circ = plt.Circle((self.circumcenter.x,self.circumcenter.y),self.circumradius,color="red",fill=False)
            ax.add_patch(circ)

        return ax


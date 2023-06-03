from geom import Point, Edge, Triangle
from matplotlib import pyplot as plt

def delaunay_triangulation(points):
    # Bowuyer-Watson algorithm
    # find width and height of the given set of points
    sz = len(points)
    sorted_x = sorted(points, key = lambda point : point.x)
    sorted_y = sorted(points, key = lambda point : point.y)
    min_x = sorted_x[0].x
    max_x = sorted_x[sz-1].x
    min_y = sorted_y[0].y
    max_y = sorted_y[sz-1].y

    # add super-triangle that contains all the points inside it
    super_triangle = Triangle(Point(min_x-1,min_y-1),Point(min_x-1,min_y+2*(max_y-min_y)+10),Point(min_x+2*(max_x-min_x)+10,min_y-1))
    triangulation = []
    triangulation.append(super_triangle)

    for point in points:
        bad_triangles = []
        for triangle in triangulation:
            if triangle.point_in_circumcircle(point):
                bad_triangles.append(triangle)

        polygon = []
        for triangle in bad_triangles:
            for edge in triangle.edges:
                shared = False
                for triangle2 in bad_triangles:
                    if triangle2 != triangle:
                        for edge2 in triangle2.edges:
                            if edge == edge2:
                                shared = True
                if not shared:
                    polygon.append(edge)

        for triangle in bad_triangles:
            triangulation.remove(triangle)

        for edge in polygon:
            triangle = Triangle(edge.point1, edge.point2, point)
            triangulation.append(triangle)

    big_triangles = []
    for triangle in triangulation:
        for vertex in triangle.points:
            for super_vertex in super_triangle.points:
                if vertex == super_vertex:
                    big_triangles.append(triangle)
    
    for triangle in big_triangles:
        if triangle in triangulation:
            triangulation.remove(triangle)

    return triangulation

def plot_triangulation(triangulation, ax, with_circle=False):
    for triangle in triangulation:
        ax = triangle.plot_triangle(ax, with_circle)

    return ax


if __name__ == "__main__":
    points = [Point(1,1),Point(2,4),Point(-3,2),Point(6,3),Point(-2.4,3.7),Point(1.5,-2.6),Point(0.2,0.1), Point(0.4,2)]

    triangulation = delaunay_triangulation(points)
    fig, ax = plt.subplots()
    ax = plot_triangulation(triangulation, ax, True)
    ax.set_aspect("equal")
    plt.show()

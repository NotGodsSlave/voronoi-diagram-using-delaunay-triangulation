from geom import Point, Edge, Triangle
from matplotlib import pyplot as plt
import argparse

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
    super_triangle = Triangle(Point(min_x-10,min_y-10),Point(min_x-10,min_y+2*(max_y-min_y)+100),Point(min_x+2*(max_x-min_x)+100,min_y-10))
    triangulation = []
    triangulation.append(super_triangle)

    for point in points:
        # add points one by one, removing all triangles with circumcircles containing the point and adding new triangles with the point
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

    # remove triangles containing supertriangle vertices
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
    parser = argparse.ArgumentParser(description="Plot Voronoi diagram")
    parser.add_argument("points", metavar='p', type=float, nargs='+', help="list of points coordinates, each two consequtive numbers correspond to one point")
    parser.add_argument("--circles", action="store_true", help="plot Delaunay circumcircles")
    args = parser.parse_args()
    if len(args.points) % 2:
        print("As each point has two coordinates, please provide an even number of coordinates")
    else:
        points = []
        for coord in range(0, len(args.points), 2):
            points.append(Point(args.points[coord], args.points[coord+1]))
        triangulation = delaunay_triangulation(points)
        fig, ax = plt.subplots()
        ax = plot_triangulation(triangulation, ax, args.circles)
        ax.set_aspect("equal")
        plt.show()

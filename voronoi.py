from geom import Point, Edge, Line, Triangle
from delaunay import delaunay_triangulation, plot_triangulation
from matplotlib import pyplot as plt
import argparse

def plot_voronoi(points, plot_triangles = False, with_circles = False):
    triangulation = delaunay_triangulation(points)
    fig, ax = plt.subplots()
    for point in points:
        ax.plot(point.x,point.y,'bo')
    
    # determining diagram bounds
    circumcenters = [triangle.circumcenter for triangle in triangulation]
    xsorted = sorted(circumcenters, key = lambda point : point.x)
    ysorted = sorted(circumcenters, key = lambda point : point.y)
    bounds = [xsorted[0].x-5,ysorted[0].y-5,xsorted[len(xsorted)-1].x+5,ysorted[len(ysorted)-1].y+5]

    # voronoi edges are perpendicular to triangulation edges and lie between circumcenters
    voronoi_edges = dict()
    opposite_point = dict()

    voronoi_intersections = []
    for triangle in triangulation:
        voronoi_intersections.append(triangle.circumcenter)
        for index, edge in enumerate(triangle.edges):
            voronoi_edges[edge] = []
            opposite_point[edge] = triangle.points[2-index]

    for triangle in triangulation:
        for edge in triangle.edges:
            voronoi_edges[edge].append(triangle.circumcenter)

    for edge in voronoi_edges:
        if len(voronoi_edges[edge]) == 1: # border edges
            p = voronoi_edges[edge][0]
            voronoi_line = edge.get_line().find_perpendicular(edge.get_midpoint())
            # find where the line intersects bounds, select point on bound as second edge end
            # if the line is parallel to either axis finding correct direction is trivial
            if voronoi_line.a == 0:
                if opposite_point[edge].x > p.x:
                    voronoi_edges[edge].append(Point(bounds[0],p.y))
                else:
                    voronoi_edges[edge].append(Point(bounds[2],p.y))
            elif voronoi_line.b == 0:
                if opposite_point[edge].y > p.y:
                    voronoi_edges[edge].append(Point(p.x,bounds[1]))
                else:
                    voronoi_edges[edge].append(Point(p.x,bounds[3]))
            else:
                # otherwise check if circumcenter lies between opposite point and the edge
                circumcenter = voronoi_edges[edge][0]
                edge_line = edge.get_line()
                between = edge_line.same_side(circumcenter,opposite_point[edge])

                # find intersection between voronoi line and the edge
                intersection = voronoi_line.find_intersection(edge_line)

                # determine whether x on bounds needs to be lower or higher than at circumcenter
                direction = True #higher
                if (between and intersection.x < circumcenter.x) or (not between and intersection.x >= circumcenter.x):
                    direction = False #lower
                if circumcenter == intersection and opposite_point[edge].x < circumcenter.x:
                    direction = True

                # find points of intersection with the bounds
                bound_intersections = set()
                for x in [bounds[0],bounds[2]]:
                    y = -voronoi_line.a/voronoi_line.b*x - voronoi_line.c/voronoi_line.b
                    if y >= bounds[1] and y <= bounds[3]:
                        bound_intersections.add(Point(x,y))

                for y in [bounds[1],bounds[3]]:
                    x = -voronoi_line.b/voronoi_line.a*y - voronoi_line.c/voronoi_line.a
                    if x >= bounds[0] and x <= bounds[2]:
                        bound_intersections.add(Point(x,y))
                bi = list(bound_intersections)

                # find which point of intersection to use based on voronoi edge direction
                if direction:
                    if bi[0].x > bi[1].x:
                        point = bi[0]
                    else:
                        point = bi[1]
                else:
                    if bi[0].x < bi[1].x:
                        point = bi[0]
                    else:
                        point = bi[1]

                voronoi_edges[edge].append(point)
               
        if len(voronoi_edges[edge]) == 2:
            e = voronoi_edges[edge]
            ax.plot([e[0].x,e[1].x],[e[0].y,e[1].y], color="blue")  

    if plot_triangles:
        ax = plot_triangulation(triangulation, ax, with_circles)
    ax.set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Voronoi diagram")
    parser.add_argument("points", metavar='p', type=float, nargs='+', help="list of points coordinates, each two consequtive numbers correspond to one point")
    parser.add_argument("--triangulation", action="store_true", help="plot Delaunay triangulation as well")
    parser.add_argument("--circles", action="store_true", help="plot Delaunay circumcircles, only works if triangulation is also used")
    args = parser.parse_args()
    if len(args.points) % 2:
        print("As each point has two coordinates, please provide an even number of coordinates")
    else:
        points = []
        for coord in range(0, len(args.points), 2):
            points.append(Point(args.points[coord], args.points[coord+1]))
        plot_voronoi(points, args.triangulation, args.circles)
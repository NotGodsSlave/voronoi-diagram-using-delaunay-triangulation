from geom import Point, Edge, Line, Triangle
from delaunay import delaunay_triangulation, plot_triangulation
from matplotlib import pyplot as plt
import argparse

def plot_voronoi(bounds, points, plot_triangles = False, with_circles = False):
    triangulation = delaunay_triangulation(points)
    fig, ax = plt.subplots()
    for point in points:
        ax.plot(point.x,point.y,'bo')
    
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
                
                # otherwise find the closest point on voronoi line to the third triangle vertex
                # and select a point on bounds on the opposite side to it as the second voronoi edge vertex
                wrong_dir_point = voronoi_line.find_perpendicular(opposite_point[edge]).find_intersection(voronoi_line)
                
                # find points of intersection with the bounds
                x_low = bounds[0]
                y_low = -voronoi_line.a/voronoi_line.b*x_low - voronoi_line.c/voronoi_line.b
                if y_low < bounds[1] or y_low > bounds[3]:
                    y_low = bounds[1]
                    x_low = -voronoi_line.b/voronoi_line.a*y_low - voronoi_line.c/voronoi_line.a

                x_high = bounds[2]
                y_high = -voronoi_line.a/voronoi_line.b*x_high - voronoi_line.c/voronoi_line.b
                if y_high > bounds[3] or y_high < bounds[1]:
                    y_high = bounds[3]
                    x_high = -voronoi_line.b/voronoi_line.a*y_high - voronoi_line.c/voronoi_line.a
                point_low = Point(x_low,y_low)
                point_high = Point(x_high,y_high)

                if wrong_dir_point.x > p.x:
                    if x_low < x_high:
                        point = point_low
                    else:
                        point = point_high
                elif wrong_dir_point.x < p.x:
                    if x_low > x_high:
                        point = point_low
                    else:
                        point = point_high
                else:
                    if wrong_dir_point.y > p.y:
                        if y_low < y_high:
                            point = point_low
                        else:
                            point = point_high
                    else:
                        if y_low > y_high:
                            point = point_low
                        else:
                            point = point_high 

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
        bounds = [-10,-10,10,10]
        plot_voronoi(bounds,points, args.triangulation, args.circles)
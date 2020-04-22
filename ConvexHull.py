# Convex hull of a random set of points:

import numpy as np
import matplotlib.pyplot as plt

# from scipy.spatial import ConvexHull


def get_degree_all(x_arr, y_arr):
    return np.arctan2(y_arr, x_arr) * 180 / np.pi


def ccw(p1, p2, p3):
    x = [p1[0], p2[0], p3[0]]
    y = [p1[1], p2[1], p3[1]]

    S = ((x[1] - x[0]) * (y[2] - y[0])) - ((y[1] - y[0]) * (x[2] - x[0]))

    if S > 0:
        return 1  # counter clock-wise
    elif S < 0:
        return -1  # clock-wise
    else:
        return 0  # same

import pprint

def MyConvexHull(_points):
    convex_points = np.copy(_points)
    y_min_idx = 0
    for idx in range(1, np.alen(convex_points)):
        if convex_points[idx, 1] < convex_points[y_min_idx, 1]:
            y_min_idx = idx
        elif convex_points[idx, 1] == convex_points[y_min_idx, 1]:
            if convex_points[idx, 0] < convex_points[idx, 0]:
                y_min_idx = idx

    for idx in range(np.alen(convex_points)):
        if idx != y_min_idx:
            convex_points[idx, 0] -= convex_points[y_min_idx, 0]
            convex_points[idx, 1] -= convex_points[y_min_idx, 1]
    convex_points[y_min_idx] = np.array([0, 0])

    degrees = get_degree_all(convex_points[:, 0], convex_points[:, 1])

    for idx, degree in enumerate(degrees[1:]):
        degrees[idx + 1] = degree

    point_dict = {}
    for idx in range(1, np.alen(convex_points)):
        if degrees[idx] in point_dict.keys():
            x1, y1 = convex_points[idx]
            x2, y2 = point_dict[degrees[idx]][1]
            if x1**2 + y1**2 > x2**2 + y2**2:
                point_dict[degrees[idx]] = (idx, convex_points[idx])
        else:
            point_dict[degrees[idx]] = (idx, np.copy(convex_points[idx]))
    point_list = [[degrees[0], 0, np.copy(convex_points[0])]]
    for degree in point_dict:
        point_list.append([degree, point_dict[degree][0], point_dict[degree][1]])
    point_list.sort()
    """
    point_list = []
    for idx in range(np.alen(convex_points)):
        point_list.append([degrees[idx], idx, np.copy(convex_points[idx])])
    point_list.sort()
    pprint.pprint(point_list)
    """
    sorted_list = []
    for idx in range(np.alen(point_list)):
        sorted_list.append([point_list[idx][1], point_list[idx][2]])

    stack = [sorted_list[0], sorted_list[1]]
    idx = 2
    while idx < np.alen(sorted_list):
        if ccw(stack[-2][1], stack[-1][1], sorted_list[idx][1]) > 0:
            stack.append(sorted_list[idx])
            idx += 1
        else:
            stack.pop()

    result = np.array([], dtype=int)
    for idx in range(len(stack) - 1):
        result = np.append(result, np.array([stack[idx][0], stack[idx + 1][0]]))
    result = np.append(result, np.array([stack[len(stack) - 1][0], stack[0][0]]))
    result = result.reshape(int(np.alen(result) / 2), 2)

    return result


points = np.array([], dtype=int)
inp_file = open("layer3.txt", "r")
N = int(inp_file.readline())
for _ in range(N):
    line = inp_file.readline()
    points = np.append(points, np.array([int(line.split()[0]), int(line.split()[1])]))
inp_file.close()
points = points.reshape(int(np.alen(points)/2), 2)

while True:
    if np.alen(points) < 3:
        break
    #hull = ConvexHull(points)
    pprint.pprint(points)
    hull = MyConvexHull(points)

    plt.plot(points[:, 0], points[:, 1], 'o')

    last_simplex = None
    point_set = set()
    location_set = set()
    # hull = hull.simplices
    for simplex in hull:  # left src node 번호, right tgt node 번호
        plt.plot(points[simplex, 0], points[simplex, 1], 'r--', alpha=0.6)
        point_set.add(simplex[0])
        point_set.add(simplex[1])

    next_point = np.array([], dtype=int)
    for i in range(np.alen(points)):
        if not (i in point_set):
            next_point = np.append(next_point, np.array(points[i]))
    next_point = next_point.reshape(int(np.alen(next_point) / 2), 2)
    points = np.copy(next_point)
    pprint.pprint(points)

plt.show()

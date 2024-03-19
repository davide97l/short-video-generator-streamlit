'''Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
The distance between two points on the X-Y plane is the Euclidean distance (i.e., (x1 - x2)^2 + (y1 - y2)^2)^(1/2)
You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]

Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]

Assumptions
* 1 <= k <= points.length <= 104
* -10^4 < xi, yi < 10^4'''

def euclidean_dist(a, b):
    """
    :param a: (x1, y1)
    :param b: (x2, y2)
    :return: float, distance a, b
    """

points = [...]
k = 3
center = (0, 0)
distances = []
for x, y in points:
    dist = euclidean_dist((x, y), center)
    distances.append(dist)
top_k_idx = sort(distances, order='ascending')[:k]  # return indexes
close_points = points[[top_k_idx]]  # return points in top_k_idx

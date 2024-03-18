import numpy as np

normalized_polygon1 = np.array([
[0.34, 0.5],
[0.35, 0.44],
[0.38, 0.37],
[0.44, 0.32],
[0.5, 0.3],
[0.56, 0.32],
[0.62, 0.37],
[0.65, 0.44],
[0.66, 0.5],
[0.65, 0.56],
[0.62, 0.65],
[0.56, 0.7],
[0.5, 0.72],
[0.44, 0.7],
[0.38, 0.65],
[0.35, 0.56],
[0.34, 0.5]
], np.float32)

normalized_polygon3 = np.array([
[0.12, 0.5],
[0.16, 0.7],
[0.23, 0.84],
[0.3, 0.93],
[0.4, 0.97],
[0.5, 1],
[0.6, 0.97],
[0.7, 0.93],
[0.77, 0.84],
[0.84, 0.7],
[0.88, 0.5],
[0.84, 0.3],
[0.77, 0.16],
[0.7, 0.07],
[0.6, 0.03],
[0.5, 0],
[0.4, 0.03],
[0.3, 0.07],
[0.23, 0.16],
[0.16, 0.3],
[0.12, 0.5]
], np.float32)


'''normalized_polygon2 = np.array([
[0.22, 0.5],
[0.25, 0.35],
[0.33, 0.23],
[0.4, 0.17],
[0.5, 0.14],
[0.6, 0.17],
[0.67, 0.23],
[0.75, 0.35],
[0.78, 0.5],
[0.75, 0.65],
[0.67, 0.77],
[0.6, 0.83],
[0.5, 0.86],
[0.4, 0.83],
[0.33, 0.77],
[0.25, 0.65],
[0.22, 0.5]
], np.float32)


normalized_polygon3 = np.array([
[0.03, 0.5],
[0.05, 0.32],
[0.12, 0.11],
[0.2, 0],
[0.8, 0],
[0.88, 0.11],
[0.95, 0.32],
[0.97, 0.5],
[0.95, 0.68],
[0.88, 0.89],
[0.8, 1],
[0.2, 1],
[0.12, 0.89],
[0.05, 0.68],
[0.03, 0.5]
], np.float32)'''

normalized_polygon4 = np.array([
[0, 0],
[1, 0],
[1, 1],
[0, 1],
[0, 0]
], np.float32)

class PolygonShift:
    def __init__(self, vertical_shift, horizontal_shift):
        self.vertical_shift = vertical_shift
        self.horizontal_shift = horizontal_shift

# Create instances for different classes
fd1 = PolygonShift(vertical_shift=0, horizontal_shift=33)
fd2 = PolygonShift(vertical_shift=0, horizontal_shift=10)
fd3 = PolygonShift(vertical_shift=-10, horizontal_shift=-15)
fd4 = PolygonShift(vertical_shift=0, horizontal_shift=0)

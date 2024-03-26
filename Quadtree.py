import math

class Square:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def getCoords(self):
        return self.x, self.y, self.w, self.h

    def contains(self, point):
        return (
            self.x - self.w <= point.x <= self.x + self.w and
            self.y - self.h <= point.y <= self.y + self.h
        )


class QuadTree:
    def __init__(self, boundary, capacity):
        self.divided = False
        self.boundary = boundary
        self.capacity = capacity
        self.nodes = []
        self.children = [None] * 4
    
    def subdivide(self):
        x, y, w, h = self.boundary.getCoords()

        dx = w / 2
        dy = h / 2

        self.children[0] = QuadTree(Square(x + dx, y - dy, dx, dy), self.capacity)
        self.children[1] = QuadTree(Square(x - dx, y - dy, dx, dy), self.capacity)
        self.children[2] = QuadTree(Square(x + dx, y + dy, dx, dy), self.capacity)
        self.children[3] = QuadTree(Square(x - dx, y + dy, dx, dy), self.capacity)
        
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return
        
        if len(self.nodes) < self.capacity:
            self.nodes.append(point)
        else:
            if not self.divided:
                self.subdivide()

            for child in self.children:
                child.insert(point)

    def query_range(self, range_center, range_radius):
        result = []

        if not self.boundary_intersects_range(range_center, range_radius):
            return result

        for point in self.nodes:
            if self.point_in_range(point, range_center, range_radius):
                result.append(point)

        if self.divided:
            for child in self.children:
                result += child.query_range(range_center, range_radius)

        return result

    def boundary_intersects_range(self, range_center, range_radius):
        bx, by, bw, bh = self.boundary.getCoords()
        rx, ry = range_center

        return not (
            rx - range_radius > bx + bw or
            rx + range_radius < bx - bw or
            ry - range_radius > by + bh or
            ry + range_radius < by - bh
        )

    def point_in_range(self, point, range_center, range_radius):
        px, py = point.getCoords()
        rx, ry = range_center

        return math.sqrt((px - rx) ** 2 + (py - ry) ** 2) <= range_radius

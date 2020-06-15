class Object:
    def __init__(self,points):
        self.points = points
    def get_lines(self):
        return (self.points)

class Line(Object):
    def __init__(self,points):
        if len(points) != 4:
            raise Exception('Only one line can be in line')
        self.points = points
    def get_lines(self):
        return [self.points]

class Triangle(Object):
    def __init__(self,points):
        if len(points) != 6:
            raise Exception('must be provided 3 points')
        
        self.points = points

    def get_lines(self):
        return ((self.points[0],self.points[1],self.points[2],self.points[3]),(self.points[2],self.points[3],self.points[4],self.points[5]),(self.points[4],self.points[5],self.points[0],self.points[1]))


class Tetragon(Object):
    def __init__(self,points):
        if len(points) != 8:
            raise Exception('must be provided 4 points')
        
        self.points = points
    def get_lines(self):
        return ((self.points[0],self.points[1],self.points[2],self.points[3]),
                (self.points[2],self.points[3],self.points[4],self.points[5]),
                (self.points[4],self.points[5],self.points[6],self.points[7]),
                (self.points[6],self.points[7],self.points[0],self.points[1]))


class Circle:
    def __init__(self,center,radius):
        self.center = center
        self.radius = radius

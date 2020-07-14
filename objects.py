from PIL import Image        #pip install Pillow
import numpy

class Object:
    def __init__(self,points):
        self.points = points
    def get_lines(self):
        return (self.points)


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


class Sprite:
    def __init__(self,image,size,koef=128):
        file = Image.open(image)
        if size == True:
            file.thumbnail(self.size,Image.ANTIALIAS)
        else:
            file = file.resize(size)
        gray = file.convert('L')
        self.bw = gray.point(lambda x: 0 if x<koef else 255, '1')

        self.data = numpy.asarray(self.bw)

    def rotate(self,angle):
        if angle == 90:
            self.bw = self.bw.transpose(Image.ROTATE_90)
        elif angle == 180:
            self.bw = self.bw.transpose(Image.ROTATE_180)
        elif angle == 270:
            self.bw = self.bw.transpose(Image.ROTATE_270)
        else:
            self.bw = self.bw.rotate(angle)
        self.data = numpy.asarray(self.bw)
    
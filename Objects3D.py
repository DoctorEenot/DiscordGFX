from objects import Triangle





class Cube:
    def __init__(self):
        self.vertexes = ((0,0,0),#0
                    (0,1,0),#1
                    (1,1,0),#2
                    (1,0,0),#3
                    (1,1,1),#4
                    (1,0,1),#5
                    (0,0,1),#6
                    (0,1,1))#7

        self.triangles = [[self.vertexes[0],self.vertexes[1],self.vertexes[2]],
                          [self.vertexes[2],self.vertexes[3],self.vertexes[0]],
                          [self.vertexes[3],self.vertexes[2],self.vertexes[4]],
                          [self.vertexes[4],self.vertexes[5],self.vertexes[3]],
                          [self.vertexes[5],self.vertexes[4],self.vertexes[6]],
                          [self.vertexes[4],self.vertexes[7],self.vertexes[6]],
                          [self.vertexes[6],self.vertexes[7],self.vertexes[0]],
                          [self.vertexes[7],self.vertexes[1],self.vertexes[0]],
                          [self.vertexes[1],self.vertexes[4],self.vertexes[2]],
                          [self.vertexes[1],self.vertexes[7],self.vertexes[4]],
                          [self.vertexes[0],self.vertexes[3],self.vertexes[5]],
                          [self.vertexes[0],self.vertexes[5],self.vertexes[6]]]

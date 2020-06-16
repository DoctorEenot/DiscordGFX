import DiscordGFX
from objects import Triangle
import Objects3D


class Viewport:
    def __init__(self,size,d):
        self.size = size
        self.d = d

def sumVectors(v1,v2):
    if len(v1) != len(v2):
        raise Exception('vectors must have same lengths')
    to_return = []
    for i in range(len(v1)):
        to_return.append(v1[i]+v2[i])
    return to_return

class Engine:
    def __init__(self,screen_size=(152,39),filler='□',pixels='■',border='-',viewport_size=(1,1),d=1):
        self.screen = DiscordGFX.Screne(screen_size,filler,border)
        self.viewport = Viewport(viewport_size,d)
        self.pixels = pixels

    def TranslateToScreen(self,x,y):
        return [int((self.screen.size[0]/2)+x),int((self.screen.size[1]/2)+y)]

    def ViewportToScreen(self,x,y):
        return (x*self.screen.size[0]/self.viewport.size[0],y*self.screen.size[1]/self.viewport.size[1])
    
    def ProjectVertex(self,vertex):
        return self.ViewportToScreen(vertex[0]*self.viewport.d/vertex[2],vertex[1]*self.viewport.d/vertex[2])

    def renderModel(self,object,position,fill=False):
        for triangle in object.triangles:
            points = []
            for vec in triangle:
                moved = sumVectors(vec,position)
                projected = self.ProjectVertex(moved)
                transalted = self.TranslateToScreen(projected[0],projected[1])
                points.append(transalted[0])
                points.append(transalted[1])
            tria = Triangle(points)
            self.screen.draw_object(tria,self.pixels,fill)
    



if __name__ == '__main__':
    Gr = Engine(viewport_size=(2,2),d=1.2)

    cube = Objects3D.Cube()
    DiscordGFX.time.sleep(5)

    step = 0.1

    y = -1.5
    while y<=1.5:
        x = -1
        while x<= 0:
            Gr.screen.fill()
            Gr.renderModel(cube,[x,y,1.5])
            Gr.screen.print(1.5,sides=False)
            #DiscordGFX.time.sleep(1.5)
            x+=step
        y+=step
    

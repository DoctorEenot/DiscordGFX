from win32clipboard import * #pip install pywin32
import pyautogui             #pip install pyautogui
import time                  
import math
import objects
#from PIL import Image        #pip install Pillow
#import numpy                 #pip install numpy




class Screne:
    def __init__(self,size=(152,39),filler = None,border=None):
        #(152,39) standart size for full oppened discord window
        self.size = size
        if filler != None:
            if len(filler) > 7:
                raise Exception('filler must be 1 character')
            self.filler = filler
        else:
            self.filler = ' '


        self.border = border
        
        self.scene = [self.filler]*(size[0]*size[1])

    def convert_to_absolute(self,x,y) -> int:

        return y*self.size[0] + x

    def get_pixel(self,x,y) -> str:
        return self.scene[self.convert_to_absolute(x,y)]

    def set_pixel(self,x,y,value='■'):
        if len(value) > 1:
            raise Exception('value must be 1 character')
        
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return

        self.scene[self.convert_to_absolute(x,y)] = value
        

    def set_to_clipboard(self,value:str):
        OpenClipboard()
        EmptyClipboard()
        SetClipboardText(value,CF_UNICODETEXT)
        CloseClipboard()


    def copy(self):
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')

    
    def print(self,timeout=1,sides=True):
        '''
        Only for screen!
        '''

        if self.border != None:
            horizontal_border = f'{self.border}'*self.size[0]
            self.set_to_clipboard(horizontal_border)
            self.copy()
            if sides:
                for y in range(0,self.size[1]):
                    self.set_pixel(0,y,self.border)
                    self.set_pixel(self.size[0]-1,y,self.border)
       
        
        if self.size[0]*self.size[1]<=2000:            
            buf = ''.join(self.scene[0:self.size[0]])+'\n'
            for y in range(1,self.size[1]):
                for x in range(self.size[0]):
                    buf += self.get_pixel(x,y)
                #if y != self.size[1]:
                buf += '\n'
            self.set_to_clipboard(buf)
            self.copy()
        else:
            max_y = 2000//self.size[0]
            if max_y * self.size[0] + max_y > 2000:
                max_y -= 1
            offset = 0
            offset_up = max_y
            while offset != self.size[1]:
                buf = ''
                for y in range(offset,offset_up):
                    for x in range(self.size[0]):
                        buf += self.get_pixel(x,y)
                    buf += '\n'
                self.set_to_clipboard(buf)
                self.copy()
                offset = offset_up
                
                if self.size[1]-offset_up>max_y:
                    offset_up+=max_y
                else:
                    offset_up = self.size[1]
                
                time.sleep(timeout)

        #if self.border != None:
        #    self.set_to_clipboard(horizontal_border)
        #    self.copy()

    def fill(self):
        self.scene = [self.filler]*(self.size[0]*self.size[1])

    def draw_circle(self,circle:objects.Circle,value:str,fill=False):
        x = circle.radius
        y = 0
        radius_error = 1 - x
        while x >= y:
            self.set_pixel(x + circle.center[0],y + circle.center[1],value)
            self.set_pixel(y + circle.center[0],x + circle.center[1],value)

            self.set_pixel(-x + circle.center[0],y + circle.center[1],value)
            self.set_pixel(-y + circle.center[0],x + circle.center[1],value)

            self.set_pixel(-x + circle.center[0],-y + circle.center[1],value)
            self.set_pixel(-y + circle.center[0],-x + circle.center[1],value)

            self.set_pixel(x + circle.center[0],-y + circle.center[1],value)
            self.set_pixel(y + circle.center[0],-x + circle.center[1],value)
            
            if fill:
                for i in range(-x + circle.center[0]+1,x + circle.center[0]):
                    self.set_pixel(i,y + circle.center[1],value)
                    self.set_pixel(i,-y + circle.center[1],value)
                for i in range(-y + circle.center[0]+1,y + circle.center[0]):
                    self.set_pixel(i,x + circle.center[1],value)
                    self.set_pixel(i,-x + circle.center[1],value)
                
            y += 1
            if radius_error < 0:
                radius_error += 2*y + 1
            else:
                x -= 1
                radius_error += 2*(y-x+1)
        
    def draw_filled_triangle(self,object:objects.Triangle,value='■'):
        P0 = (object.points[0],object.points[1])
        P1 = (object.points[2],object.points[3])
        P2 = (object.points[4],object.points[5])

        if P1[1] < P0[1]:
            P_buf = P0
            P0 = P1
            P1 = P_buf
        if P2[1] < P0[1]:
            P_buf = P0
            P0 = P2
            P2 = P_buf
        if P2[1] < P1[1]:
            P_buf = P1
            P1 = P2
            P2 = P_buf

        a2 = (P1[1]-P0[1])/(P1[0]-P0[0])
        b2 = P0[1] - a2*P0[0]

        a1 = (P2[1]-P0[1])/(P2[0]-P0[0])
        b1 = P0[1] - a1*P0[0]

        if P0[0] < P1[0]:
            side = -1
        else:
            side = +1


        for y in range(P0[1],P2[1]+1):
            if y == P1[1]:
                a2 = (P2[1]-P1[1])/(P2[0]-P1[0])
                b2 = P1[1] - a2*P1[0]

            x1 = int(((y-b1)/a1))+side
            x2 = int(((y-b2)/a2))-side
            if x2 < x1:
                buf = x2
                x2 = x1
                x1 = buf
            
            for x in range(x1,x2):
                self.set_pixel(x,y,value)

    def draw_line(self,line,value='■'):
        '''
        line = (x1,y1,x2,y2)
        '''
        steep = math.fabs(line[3]-line[1]) > math.fabs(line[2]-line[0])
        if steep:
            x0 = line[1]
            y0 = line[0]
            x1 = line[3]
            y1 = line[2]
        else:
            x0 = line[0]
            y0 = line[1]
            x1 = line[2]
            y1 = line[3]

        if x0 > x1:
            b = x0
            x0 = x1
            x1 = b

            b = y0
            y0 = y1
            y1 = b

        dx = x1 - x0
        dy = math.fabs(y1-y0)
        error = dx // 2
        if (y0 < y1):
            ystep = 1
        else:
            ystep = -1

        y = y0

        for x in range(x0,x1+1):
            if steep:
                self.set_pixel(y,x,value)
            else:
                self.set_pixel(x,y,value)

            error -= dy
            if error < 0:
                y += ystep
                error += dx    

    def draw_object(self,object:objects.Object,value='■',fill = False):
        if type(object) == objects.Circle:
            self.draw_circle(object,value,fill)
            return
        elif type(object) == objects.Triangle and fill:            
            self.draw_filled_triangle(object,value)
            return


        for line in object.get_lines():
            self.draw_line(line)
    
    
    def set_sprite(self,sprite:objects.Sprite,position,value='■',rev=False):
        for y in range(len(sprite.data)):
            for x in range(len(sprite.data[y])):
                point = sprite.data[y][x]
                if not rev:
                    point = not point
                if point:
                    self.set_pixel(x+position[0],y+position[1],value)
        
                    
             




if __name__ == '__main__':
    scene = Screne(filler = '□',border = '■')
    pent = objects.Sprite('pent.jpg',scene.size)
    scene.set_sprite(pent,(0,0),rev = False)
    time.sleep(5)
    scene.print()
    
    

    

    



                


    




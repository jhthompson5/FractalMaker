#import turtle
import tkinter
import copy
import math
import time
import threading
#turtle.screensize(1200,800)
#turtle.hideturtle()




class pointer():
    def __init__(self,x=0,y=0,heading=0):
        self.x=x
        self.y=y
        self.heading=heading

    def close_window(self,_event):
        master.destroy()

    def position(self):
        return [self.x,self.y]

    def setHeading(self,heading):
        self.heading=heading

    def heading(self):
        return self.heading

    def origin():
        self.x = 0
        self.y = 0

    def NextfromHeading(self,heading,baseStep):
        [x0,y0] = self.position()
        theta = heading * math.pi/180
        x = x0 + baseStep * math.cos(theta)
        y = y0 + baseStep * math.sin(theta)
        return [x,y]       

    def setPosition(self,pos):
        self.x=pos[0]
        self.y=pos[1]

    def setx(self,x):
        self.x = x
    def sety(self,y):
        self.y = y

    def xcor(self):
        return self.x

    def ycor(self):
        return self.y

    def getLinePoints(self,points):
        points = [[x+canvas.winfo_width()/2,(canvas.winfo_height()/2-y)] for [x,y] in points]

        is_first = True
        x0 = x1 = y0 = y1 = 0
        for [x,y] in points:
            if is_first:
                x0,y0 = x,y
                is_first = False
            else:
                yield x0,y0,x,y
                x0,y0 = x,y

    def drawLines(self,points,width=2):
        for (x0,y0,x1,y1) in self.getLinePoints(points):
            canvas.create_line(x0,y0,x1,y1,width=width)
            master.update()
        self.setPosition(points[-1])

    def drawLinefromHeadings(self,baseStep,headings,width=2):
        line = [self.position()]
        for h in headings:
            line.append(self.NextfromHeading(h,baseStep))
        self.drawLines(line,width)

    def exitonclick(self):       
        canvas.bind('<ButtonRelease-1>',self.close_window)
        canvas.pack()
        master.update()
        canvas.mainloop()
        
       
class Curve():
    def __init__(self,difference1=90,difference2=None,reverse1=False,reverse2=None,initialStep=[[180]],
                    x=0,y=0, connectorAngle=None, deltaAngle=0):
        self.difference1 = difference1
        self.connectorAngle = connectorAngle
        self.deltaAngle = deltaAngle
        if difference2 == None:
            self.difference2 = difference1
        else:
            self.difference2 = difference2
        self.reverse1 = reverse1
        if reverse2 == None:
            self.reverse2 = reverse1
        else:
            self.reverse2 = reverse2
        self.initialStep = initialStep
        self.stepNumber = 0
        self.x = x
        self.y = y

    def nextStep(self,steps):
        self.stepNumber += 1 
        temp = []
        temp2 = []
        for step in steps:
            for i in step:
                if self.stepNumber%2 == 1:
                    angle = (i + self.difference1) % 360
                else:
                    angle = (i + self.difference2) % 360
                temp2.append(angle)
            temp.append(temp2)
            temp2 = []
        if (self.reverse1 and self.stepNumber%2==1) or (self.reverse2 and self.stepNumber%2==0): # if odd step and reverse1 or                                                                                                
            return deepReverse(temp)                                                             # even step and reverse2,                                                                                             
        else:                                                                                    # reverse order of steps performed
            return temp


'''def close_window(_a):
    master.destroy()'''

def deepReverse(p):
    p.reverse()
    for i in p:
        if type(i) == type(list()):
            deepReverse(i)
    return p

def HochInit(cx=-150,cy=-200,heading=0):
    return Curve(difference1=60, difference2=-60,reverse1=False, initialStep=[[heading]], x=cx, y=cy)

def DragonInit(heading=180,cx=0,cy=0):
    return Curve(difference1=-90, reverse1=True, initialStep=[[heading]], x=cx, y=cy)

def LevyInit(heading=180,cx=0,cy=0):
    return Curve(difference1=90, reverse1=False, initialStep=[[heading]], x=cx, y=cy)

def HilbertInit(heading=0, cx=0, cy=0):   # Does not work at the moment
    return Curve(difference1=-90, difference2=0,reverse1=True,reverse2=False,initialStep=[[heading, (heading+90)%360, (heading+180)%360]],connectorAngle=heading+90,deltaAngle=-90)






master = tkinter.Tk()
canvas = tkinter.Canvas(master,width=1200, height=800)
canvas.pack()
master.update()


levy = LevyInit()
dragon = DragonInit()
hoch = HochInit()

turtle = pointer()

def draw(mode = levy, count=1, baseStep=3,numIters=12):
    steps = mode.initialStep
    connectorAngle = mode.connectorAngle
    width = 2
    if count==1:
        #turtle.penup()

        turtle.setx(mode.x)
        turtle.sety(mode.y)
        #turtle.setheading(mode.initialStep[0][0])
        #turtle.pendown()
        draw(mode,count+1,baseStep,numIters)
    else:
        if count <= numIters:
            newSteps = mode.nextStep(steps)
            for i in newSteps:
                steps.append(i)  
            draw(mode,count+1,baseStep,numIters)
        else:
            for step in steps:
                turtle.drawLinefromHeadings(baseStep,step,width)
                #for i in step:
                #    turtle.setheading(i)
                #    turtle.forward(baseStep)
                #if mode.connectorAngle:
                #    turtle.setheading(connectorAngle)
                #    turtle.forward(baseStep)
                #    connectorAngle += mode.deltaAngle
                

def drawSnowflake(x=-300,y=150,heading=0,baseStep=2,numIters=9):
    turtle.setx(x)
    turtle.sety(y)
    for i in range(3):
        hoch = HochInit(turtle.xcor(),turtle.ycor(),(heading-120*i)%360)
        draw(hoch, 1, baseStep, numIters)
    '''
    hoch = HochInit(cx=turtle.xcor(),cy=turtle.ycor(),heading=240)
    draw(hoch, 1, baseStep, numIters)
    hoch = HochInit(cx=turtle.xcor(),cy=turtle.ycor(),heading=120)
    draw(hoch, 1, baseStep, numIters)'''

#Example calls of the other curves
#draw(mode=dragon,baseStep=3,numIters=12)

#draw(mode=levy)

def showHochGrowth(): #Shows how hoch curve grows as the number of iterations increases
    exp = 2
    for i in range(7,18,2):
        hoch = HochInit(-150,200-(i-7)*50,0)
        draw(mode=hoch,numIters=i,baseStep=121.5/(3**exp))
        exp += 1
    turtle.exitonclick()

#showHochGrowth()

def drawHexagon(numIters,baseStep,x,y):
    exp = (numIters-3)/2 + 1
    xDif = baseStep * (3**exp)
    yDif = 1/3 * xDif * math.sin(math.pi/3) 
    turtle.setx(x)
    turtle.sety(y)
    for i in range(6):  
        Hoch = HochInit(cx=turtle.xcor(), cy=turtle.ycor(), heading=(60*i)%360)
        draw(Hoch,baseStep=baseStep,numIters=numIters)


def drawHexaflake(numIters=9,cx=-200,cy=100):
    baseStep = 4 * 3**((9-numIters)/2)
    exp = (numIters-3)/2 + 1
    xDif = baseStep * (3**exp)
    yDif = 1/3 * xDif * math.sin(math.pi/3)
    drawHexagon(numIters,baseStep,cx,cy-4*yDif)    
    drawSnowflake(cx,cy,0,baseStep,numIters=numIters)
    snowflakes = [[cx,cy]]
    nextFlakes = []
    
    
    while numIters > 3:       
        numIters -= 2
        temp = []
        for i in snowflakes:
            
            x1 = i[0]
            y1 = i[1]+ 4/3 * yDif
            
            x2 = x1 + 2/3*xDif
            y2 = y1

            x3 = x1
            y3 = y1 - 4*yDif

            x4 = x2
            y4 = y3

            x5 = x1 - 1/3*xDif
            y5 = y1 - 2*yDif
            
            x6 = x2 + 1/3*xDif
            y6 = y5 
            


            nextFlakes.append([[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5],[x6,y6]])
        for ring in nextFlakes:
            for flake in ring:
                drawSnowflake(x=flake[0],y=flake[1],baseStep=baseStep,numIters=numIters)
        snowflakes = []
        for i in nextFlakes:
            for k in i:
                snowflakes.append(k)
        nextFlakes = []
        exp = (numIters-3)/2 + 1
        xDif = baseStep * (3**exp)
        yDif = 1/3 * xDif * math.sin(math.pi/3)

#drawHexaflake(9)  # fractal of a fractal
#hoch = HochInit(-600,-200,0)
#draw(hoch,baseStep=2,numIters=13)
drawHexaflake(numIters=5)

turtle.exitonclick()
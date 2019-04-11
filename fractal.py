import turtle
import copy
import math

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

levy = LevyInit()
dragon = DragonInit()
hoch = HochInit()

def draw(mode = levy, count=1, baseStep=3,numIters=12):
    steps = mode.initialStep
    connectorAngle = mode.connectorAngle
    if count==1:
        turtle.penup()
        turtle.screensize(1200,800)
        turtle.hideturtle()
        turtle.pensize(2)
        turtle.speed(0)
        turtle.setx(mode.x)
        turtle.sety(mode.y)
        turtle.setheading(mode.initialStep[0][0])
        turtle.pendown()
        draw(mode,count+1,baseStep,numIters)
    else:
        if count <= numIters:
            newSteps = mode.nextStep(steps)
            for i in newSteps:
                steps.append(i)  
            draw(mode,count+1,baseStep,numIters)
        else:
            for step in steps:
                for i in step:
                    turtle.setheading(i)
                    turtle.forward(baseStep)
                if mode.connectorAngle:
                    turtle.setheading(connectorAngle)
                    turtle.forward(baseStep)
                    connectorAngle += mode.deltaAngle
                

def drawSnowflake(x=-300,y=150,heading=0,baseStep=2,numIters=11):
    hoch = HochInit(x,y,heading)
    draw(hoch, 1, baseStep, numIters)
    hoch = HochInit(cx=turtle.xcor(),cy=turtle.ycor(),heading=240)
    draw(hoch, 1, baseStep, numIters)
    hoch = HochInit(cx=turtle.xcor(),cy=turtle.ycor(),heading=120)
    draw(hoch, 1, baseStep, numIters)

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

def drawHexaflake(numIters=9):
    baseStep = 4
    drawSnowflake(-200,100,0,baseStep,numIters=numIters)
    snowflakes = [[-200,100]]
    nextFlakes = []
    
    
    while numIters > 3:
        exp = (numIters-3)/2 + 1
        xDif = baseStep * (3**exp)
        yDif = 1/3 * xDif * math.sin(math.pi/3)
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


drawHexaflake()  # fractal of a fractal



turtle.exitonclick() # After all drawing commands. Hold screen open. Dismiss on mouse click



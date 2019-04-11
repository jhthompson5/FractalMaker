import turtle
import copy

class Curve():
    def __init__(self,difference1=90,difference2=None,reverse=False,initialStep=[[180]],x=0,y=0):
        self.difference1 = difference1
        if difference2 == None:
            self.difference2 = difference1
        else:
            self.difference2 = difference2
        self.reverse = reverse
        self.initialStep = initialStep
        self.stepNumber = 1
        self.x = x
        self.y = y
    
    def nextStep(self,steps):
        temp = []
        for step in steps:
            if self.stepNumber%2 == 1:
                angle = (step[0] + self.difference1) % 360
            else:
                angle = (step[0] + self.difference2) % 360
            temp.append(angle)

        if self.reverse:
            ret = reversed([[i] for i in temp])
        else:
            ret = [[i] for i in temp]
        self.stepNumber += 1
        return ret

def HochInit():
    return Curve(difference1=60, difference2=-60,reverse=False, initialStep=[[0]],x=-200,y=-100)

def DragonInit():
    return Curve(difference1=-90,reverse=True,initialStep=[[180]])

def LevyInit():
    return Curve(difference1=90,reverse=False,initialStep=[[180]])


levy = LevyInit()
dragon = DragonInit()
hoch = HochInit()

def draw(mode = levy, count=1, baseStep=3,numIters=12):
    steps = mode.initialStep
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
                turtle.setheading(step[0])
                turtle.forward(baseStep)
                

draw(mode=dragon,baseStep=2)
#draw(mode=levy)
'''exp = 0
for i in range(3,10,2):
    draw(mode=hoch,numIters=i,baseStep=162/(3**exp))
    hoch = HochInit()
    exp += 1'''

turtle.exitonclick()
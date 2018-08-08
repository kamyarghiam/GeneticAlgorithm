# Updated Animation Starter Code

from tkinter import *
import random
import math
import numpy 
from generations import * 

def init(data):
    # load data.xyz as appropriate
    data.lamps = []
    data.dots = []
    for i in range(20):
        for j in range(20):
            cx = 25*i +12.5
            cy = 25*j + 12.5
            data.dots.append([cx,cy, "N/A"])
    brightnessForAllG500 = [False]
    while brightnessForAllG500[0] == False:
        #adds random lamps until it reaches minimum brightness
        data.lamps.append(Lamp(data))
        brightnessForAllG500 = checkBrightness500(data.lamps, data)
    BI = brightnessForAllG500[1]
    #SD over 2

    totalCost = []
    for lamp in data.lamps:
        totalCost.append(lamp.cost)
    standardDeviation = (numpy.std(BI))/22
    BIaverage = (sum(BI)/len(BI))/4
    cost = (sum(totalCost))/20016

    return [BIaverage, standardDeviation, cost]



def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    for i in range(20):
        canvas.create_line(i*25, 0, i*25, 500)
        canvas.create_line(0, i*25, 500, i*25)
    for i in data.dots:
        cx = i[0]
        cy = i[1]
        canvas.create_oval(cx-1, cy-1, cx+1, cy+1, width = 1, outline = "black", fill = "black")
        try: 
            canvas.create_text(cx,cy+4, text = "%0.02f" % i[2], font = "Helvitica 7")
        except: continue

    canvas.create_rectangle(data.r1,width = 0, fill = "brown")
    canvas.create_rectangle(data.r2,width = 0 , fill = "brown")
    canvas.create_rectangle(data.r3, width = 0, fill = "brown")
    for i in data.lamps:
        i.drawLamp(canvas)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()

    scoresAndLamps = dict()



    #CONTROL CENTER 
    numPeople = 100 #originial gen
    generations = 30
    mutationRate = 4 #percent
    data.r1 = [200,300,250, 350]
    data.r2 = [100,100,150, 150]
    data.r3 = [350,150,400, 190]
    #CONTROl CENTER




    takesSeconds = (.32*numPeople)*generations
    print("This simulation will take about %d seconds" % takesSeconds)
    for i in range(numPeople):
        print("Original generation baby %d out of %d" %(i, numPeople))
        result = init(data)
        BI = result[0]*1000
        SD = result[1]*1000
        C = result[2]*1000
        fit = BI - SD - C
        scoresAndLamps[fit] = data.lamps
    maxfit = None
    for fitIndex in scoresAndLamps:
        if maxfit == None or fitIndex > maxfit:
            maxfit = fitIndex
    print("Starting maxfit is %0.2f" % maxfit)  
    data.lamps = runGeneration(scoresAndLamps, numPeople, generations, data, mutationRate)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run(500, 500)
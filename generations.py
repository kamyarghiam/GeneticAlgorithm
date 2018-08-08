# Updated Animation Starter Code
import random
import math
import numpy 
import copy


def runGeneration(lampsDict, numPeople, generations, data, mutationRate):
    newGen = []
    maxfit = None
    maxroom = None
    for i in range(generations):
        maxfit = None
        maxroom = None
        newGen = []
        print("generation %d out of %d" % (i, generations))
        totalFitness = 0
        minFit = None
        for fitness in lampsDict:
            if minFit == None or fitness < minFit:
                minFit = fitness
        for fitness in lampsDict:
            totalFitness += fitness - minFit

        cumuProb = []
        rooms = []
        cumulativeProb = 0
        
        for fitness in lampsDict:
            newFit = fitness - minFit
            probability = (newFit/totalFitness)*100 + cumulativeProb
            cumulativeProb = probability
            cumuProb.append(probability)
            rooms.append(lampsDict[fitness])
        fitnesses = []
        trial = 1
        tempRooms = copy.deepcopy(rooms)
        while len(fitnesses) < numPeople:
            rooms = copy.deepcopy(tempRooms)
            print("Making baby %d out of %d" % (len(fitnesses), numPeople))
            lampAndFitness = makeBaby(cumuProb, rooms, data, mutationRate)
            if lampAndFitness == None:
                print("Room did not survive, trial: %d" % trial)
                trial += 1
            else:
                trial = 1
                newGen.append(lampAndFitness[0])
                fitnesses.append(lampAndFitness[1])
        lampsDict.clear()
        for i in range(len(newGen)):
            lampsDict[fitnesses[i]] = newGen[i]
        for fitIndex in lampsDict:
            if maxfit == None or fitIndex > maxfit:
                maxfit = fitIndex
                maxroom = lampsDict[fitIndex]

        print("MaxFit = %0.2f" % maxfit)
    return maxroom

def checkBrightness500(lamps, data):
    BI = []
    for i in range(len(data.dots)):
        if dotInsideBox(data,data.dots[i]):
            continue
        index = brightNessIndex(data.dots[i], lamps, data) 
        BI.append(index)       
        if brightNessIndex(data.dots[i], lamps, data) == None:
            return [False]
        else:
            data.dots[i][2] = index
    return [True, BI]

def makeBaby(cumuProb, rooms, data, mutationRate):

    dad = random.random()*100
    #don't want them to be equal 
    for i in range(len(cumuProb)):
        if cumuProb[i] > dad:
            dad = rooms[i]
            break
    mom = dad 
    trialCount = 0
    while mom == dad:
        trialCount += 1
        #print(cumuProb)
        momIndex = random.random()*100
        for j in range(len(cumuProb)):
            if cumuProb[j] > momIndex:
                #print(cumuProb[j])
                mom = rooms[j]
                break
        if trialCount > 100:
            return None
    newLamps = set()
    brightnessForAllG500 = [False]
    while brightnessForAllG500[0] == False:
        randNum = random.randint(0,1)
        if len(dad) == 0:
            randNum = 1
            if len(mom) == 0:
                print("oops")
        if len(mom) == 0:
            randNum = 0
        if randNum == 0:
            #select a lamp from dad
            randNum = random.randint(0,len(dad)-1)
            newLamps.add(dad[randNum])
            dad.pop(randNum)
        else:
            #select a lamp from mom
            randNum = random.randint(0,len(mom)-1)
            newLamps.add(mom[randNum])
            mom.pop(randNum)
        #check if all 500
        brightnessForAllG500 = checkBrightness500(list(newLamps), data)
    BI = brightnessForAllG500[1]

    newLamps = list(newLamps)
    #mutate lamps
    mutation = False
    for lamp in newLamps:
        #location 
        randNum = random.randint(0,99)
        if randNum < mutationRate:
            mutation = True
            print("Mutation of location!")
            x = lamp.x
            y = lamp.y
            inrange = False
            trialCounter = 0
            while inrange == False:
                trialCounter += 1
                newx = x + numpy.random.normal(scale = 10)
                newy = y + numpy.random.normal(scale = 10)
                if (newx > 5 and newx < 450) and (newy > 5 and newy < 450):
                    inrange = True
                    lamp.x = newx
                    lamp.y = newy
                if trialCounter > 70:
                    return None
        #brightness
        randNum = random.randint(0,99)
        if randNum < mutationRate:
            mutation = True
            print("Mutation of brightness!")
            bright = lamp.lumens
            inrange = False
            trialCounter2 = 0
            while inrange == False:
                trialCounter2 += 1
                newbright = bright + numpy.random.normal(scale = 20)
                if (lamp.lumens > 1500 and lamp.lumens < 4000):
                    inrange = True
                    lamp.lumens = newbright
                if trialCounter2 > 70:
                    return None
    if mutation:
        brightnessForAllG500 = checkBrightness500(newLamps, data)

        if brightnessForAllG500[0] == False:
            print("Mutation hurt offspring")
            return None
    totalCost = []
    for lamp in data.lamps:
        totalCost.append(lamp.cost)
    standardDeviation = (numpy.std(BI))/22
    BIaverage = (sum(BI)/len(BI))/4
    cost = (sum(totalCost))/20016

    result = [BIaverage, standardDeviation, cost]
    BI = result[0]*1000
    SD = result[1]*1000
    C = result[2]*1000
    fit = BI - SD - C
    # [lamps, fitness]
    return [newLamps, fit]
                
            
   


class Lamp(object):
    def __init__(self, data):
        self.x = random.randint(5,450)
        self.y = random.randint(5,450)
        self.lumens = random.randint(1500, 4000)
        self.cost = (self.lumens-1500)/2500
        while dotInsideBox(data, [self.x,self.y]):
            self.x = random.randint(5,450)
            self.y = random.randint(5,450)
    def drawLamp(self,canvas):
        canvas.create_oval(self.x-4,self.y-4, self.x+4, self.y+4, width = self.lumens/2000, outline = "red", fill = "yellow")

    def __repr__(self):
        return "Lamp at (%0.02f, %0.02f) with %d brightness and %0.1f cost" % (self.x, self.y, self.lumens, self.cost)
####################################
# customize these functions
####################################

#check this again
def rectIntersect(tlx, tly, brx, bry, x1, y1, x2, y2):
    if x1 == x2:
        if x1 >= tlx and x1<= brx:
            return True
    if y1 == y2:
        if y1 >= tly and y1 <= bry:
            return True 
    tlx, tly = tly, tlx
    brx, bry = bry, brx
    x1, y1 = y1, x1
    x2, y2 = y2, x2

    m = (y2-y1)/(x2-x1)
    b = y2-m*x2

    lefty = m*(tlx)+b
    righty = m*(brx)+b
    topx = (tly-b)/m
    botx = (bry-b)/m
    if (lefty <= tly and lefty >= bry) or (righty <= tly and righty >= bry):
        return True
    if (topx >= tlx and topx <= brx) or (botx >= tlx and botx <= brx):
        return True
    return False

def distFor(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

#dot = [x,y]   
#lamps = [lamp1, lamp2...]
def brightNessIndex(dot, lamps, data):
    totalBright = 0 
    for lamp in lamps:
        if not (rectIntersect(data.r1[0], data.r1[1], data.r1[2],data.r1[3],dot[0],dot[1],lamp.x,lamp.y) or rectIntersect(data.r2[0], data.r2[1], data.r2[2],data.r2[3],dot[0],dot[1],lamp.x,lamp.y) or rectIntersect(data.r3[0], data.r3[1], data.r3[2],data.r3[3],dot[0],dot[1],lamp.x,lamp.y)):
            distance = distFor(dot[0],dot[1], lamp.x, lamp.y)/500
            brightness = lamp.lumens/(4*math.pi*(distance**2))
            totalBright += brightness
    if totalBright < 500:
        return None
    return (-math.atan(.02*(totalBright-500)) + math.pi/2)/1.5

def dotInsideBox(data, dot):
    return ((data.r1[0] <= dot[0] <= data.r1[2]) and (data.r1[1] <= dot[1] <= data.r1[3])) or ((data.r2[0] <= dot[0] <= data.r2[2]) and (data.r2[1] <= dot[1] <= data.r2[3])) or ((data.r3[0] <= dot[0] <= data.r3[2]) and (data.r3[1] <= dot[1] <= data.r3[3]))

class Struct(object): pass
data = Struct()
data.r1 = [300,300,350, 350]
data.r2 = [100,100,150, 150]
data.r3 = [350,150,400, 190]


####################################
# use the run function as-is
####################################

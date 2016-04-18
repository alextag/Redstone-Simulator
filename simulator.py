from world import *
from tile import *
MAP_SIZE = 7
MAX_RAD = 5
class sim():

    def __init__(self,filename="NEW"):
        self.w = world(filename)

    def run(self):
        ans = ""
        while not ans in ['q','e']:
            if ans != "show":
                print(self.w)
            ans = input("Next: ")
            if ans in ['c','C']:
                x = "-1"
                while int(x)<0 or int(x)>=MAP_SIZE:
                    x = input("x: ")
                y = "-1"
                while int(y)<0 or int(y)>=MAP_SIZE:
                    y = input("y: ")
                to = input("to: ")
                prev = self.w.map[int(x)][int(y)].type
                self.w.change(int(x),int(y),to)
                #self.work(int(x),int(y),prev)
            elif ans=="clear":
                self.w._clear()
            elif ans=="depower":
                self.w.depower()
            elif ans=="resolve":
                self.w.depower()
                for i in self.w.torches:
                    x = i[0]
                    y = i[1]
                    if self.w.map[x][y].onbox == 'a':
                        close = [(x+1,y),(x-1,y),(x,y+1)]
                    elif self.w.map[x][y].onbox == 's':
                        close = [(x-1,y),(x,y+1),(x,y-1)]
                    elif self.w.map[x][y].onbox == 'd':
                        close = [(x+1,y),(x-1,y),(x,y-1)]
                    elif self.w.map[x][y].onbox == 'w':
                        close = [(x+1,y),(x,y+1),(x,y-1)]
                    for (x,y) in close:
                        self.backtrace(x,y,1)
                    self.resolve(i,1)
                for i in self.w.torches_low_priority:
                    self.backtrace(i[0],i[1],1)
                    self.resolve(i,1)
            elif ans=="show":
                self.w.show()
            elif ans=="torches":
                for i in self.w.torches_low_priority:
                    print (self.w.map[i[0]][i[1]].onbox)
    
    #The function that empowers all the system when called        
    def resolve(self, tup, rad,parent=None):
        '''(sim,tuple) -> NoneType
        Takes a (x,y) tuple of a lit torch as start and resolves network.
        One must first depower the whole system.'''
        #If the signal traveled more than 4 blocks without a repeater
        #Then kill the signal
        #-----------------
        if rad>MAX_RAD:
            return
        #-----------------
        (x,y) = tup
        if self.w.map[x][y].type == "P":
            close = [self.w.map[x][y].facing]
            parent = None
        else:
            close = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        if not parent is None:
            close.remove(parent)
        parent = (x,y)
        for (a,b) in close:
            #If the a and b are out of range just kill the recusrion.
            if a < MAP_SIZE and b < MAP_SIZE and a>=0 and b>=0:

                #If the tile in question is redstone
                if self.w.map[a][b].type == "R":
                    if rad == -1:
                            rad +=2 #If prev was repeater correct the rad
                    
                    if rad<self.w.map[a][b].range: #So that it won't get in an inf loop.
                        self.w.map[a][b].pwr = True
                        self.w.map[a][b].range = rad
                        self.resolve((a,b),rad+1,parent)

                #If the tile in question is a repeater    
                elif self.w.map[a][b].type == "P":
                    tup = self.w.map[a][b].facing
                    if self.w.map[a][b].pfrom == (x,y):
                        self.w.map[a][b].pwr = True
                        #Repeater gives a -1 radius so that the next recursive call
                        #can tell that the previous obj is a repeater
                        #So that TB doesn't work and TPB works
                        self.resolve((a,b),-1,parent)

                #If the tile in question is a block
                elif self.w.map[a][b].type == "B":
                    if not parent is None:
                        x = parent[0]
                        y = parent[1]
                        if self.w.map[x][y].type == "R":
                            print 
                            if x == a:
                                if not self.redstone_close(x,y,False):
                                    self.w.map[a][b].pwr = True
                                    self.resolve((a,b),6,parent)
                            elif y == b:
                                if not self.redstone_close(x,y,True):
                                    self.w.map[a][b].pwr = True
                                    self.resolve((a,b),6,parent)
                                    
                        elif rad == -1 and not self.w.map[a][b].pwr:#If prev was repeater, power the box
                            self.w.map[a][b].pwr = True
                            self.resolve((a,b),1,parent)

    def redstone_close(self,x,y,left):
        if left:
            return self.w.map[x][y-1].type == "R" or self.w.map[x][y+1].type == "R"
        else:
            return self.w.map[x-1][y].type == "R" or self.w.map[x+1][y].type == "R"

        
    #This function is not being used right now
    #it is just an old attempt...
    def work(self,x,y,prev):
        if self.w.map[x][y].type == "A":
            return
        
        elif self.w.map[x][y].type == "B":
            if self.check(x,y,"P"):
                print ("WORKED")
                self.w.map[x][y].pwr = True
                
        elif self.w.map[x][y].type == "T":

            if self.w.map[x-1][y].type== "P":
                self.w.map[x-1][y].pwr = True
            elif self.w.map[x+1][y].type== "P":
                self.w.map[x+1][y].pwr = True
            elif self.w.map[x][y-1].type== "P":
                self.w.map[x][y-1].pwr = True
            elif self.w.map[x][y+1].type== "P":
                self.w.map[x][y+1].pwr = True

            elif self.w.map[x+1][y].type == "R":
                self.w.map[x+1][y].pwr = True
                self.w.map[x+1][y].range = 1
            elif self.w.map[x-1][y].type == "R":
                self.w.map[x-1][y].pwr = True
                self.w.map[x-1][y].range = 1
            elif self.w.map[x][y+1].type == "R":
                self.w.map[x][y+1].pwr = True
                self.w.map[x][y+1].range = 1
            elif self.w.map[x][y-1].type == "R":
                self.w.map[x][y-1].pwr = True
                self.w.map[x][y-1].range = 1

        elif self.w.map[x][y].type == "R":
            pass
            #HERE
            
                        
        elif self.w.map[x][y].type == "P":
            
            if self.w.map[x][y].facing == (x-1,y) and self.w.map[x+1][y].pwr:
                self.w.map[x][y].pwr = True

            elif self.w.map[x][y].facing == (x+1,y) and self.w.map[x-1][y].pwr:
                self.w.map[x][y].pwr = True

            elif self.w.map[x][y].facing == (x,y+1) and self.w.map[x][y-1].pwr:
                self.w.map[x][y].pwr = True

            elif self.w.map[x][y].facing == (x,y-1) and self.w.map[x][y+1].pwr:
                self.w.map[x][y].pwr = True

    #A helper function for the "work" function
    #Not in use anymore as well....
    def check(self,x,y,typ):
        if typ == "P":
            if self.w.map[x-1][y].type == "P" and self.w.map[x-1][y].facing == (x,y) and self.w.map[x-1][y].pwr:
                return True
            if self.w.map[x+1][y].type == "P" and self.w.map[x+1][y].facing == (x,y) and self.w.map[x+1][y].pwr:
                return True
            if self.w.map[x][y-1].type == "P" and self.w.map[x][y-1].facing == (x,y) and self.w.map[x][y-1].pwr:
                return True
            if self.w.map[x][y+1].type == "P" and self.w.map[x][y+1].facing == (x,y) and self.w.map[x][y+1].pwr:
                return True
            return False
                

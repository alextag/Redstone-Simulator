from tile import *
import wx
#Map Size
MAP_SIZE = 7

class world():

    def __init__(self,filename):
        self.torches = []
        if filename == "NEW":
            self.create_world()
        else:
            self.load_world(filename)
        

    def create_world(self):
        '''(world) -> NoneType
        Create a 2-D list by creating a list that has lists in it.'''
        #Create a simple empty list
        self.map = []
        i = 0
        while i<MAP_SIZE:
            k = 0
            #Add a new element in the list, this element is also an empty list
            self.map.append([])
            while k<MAP_SIZE:
                #Add a new element in the list that you just created.
                #so our list will look somewhat like this
                #self.map = [[...],[...],...,[...],[...]]
                self.map[i].append(tile())
                k+=1
            i+=1

    def load_world(self, filename):
        '''(world, string) -> NoneType
        Load a saved world'''
        #Files must be named *.map
        #MAP_SIZE X MAP_SIZE matrix with letters {A/B/R/P/T}
        #After a "P" for repeater you must enter the direction it is facing
        # "a" --> left, "s" --> down, "d" --> right, "w" --> up
        mapfile = open(filename + ".map", "r")
        assert mapfile.readline() == "MAPSTART\n"
        currline = mapfile.readline()
        self.map = []
        i = 0
        while currline != "MAPFINISH\n":
            self.map.append([])
            times = 1
            l = 0
            rep = False
            tor = False
            for o in currline:
                if tor:
                    if o in ['a','w','s','d','n']:
                        self.map[i][l-1].onbox = o
                        self.torches.append((i,l-times))
                    times +=1
                    tor = False
                        
                if rep:
                    x=i
                    y=l-times
                    times +=1
                    to = {'a':(x,y-1),'w':(x-1,y),'d':(x,y+1),'s':(x+1,y)}
                    rev = {'a':'d','d':'a','w':'s','s':'w'}
                    self.map[i].append(repeater(to[o],to[rev[o]]))
                    rep = False     
                elif o == "A":
                    self.map[i].append(tile())
                elif o == "B":
                    self.map[i].append(block())
                elif o == "R":
                    self.map[i].append(redstone())
                    
                elif o == "T":
                    self.map[i].append(torch())
                    tor = True
                elif o == "P":
                    rep = True
                l+=1
            i+=1
            currline = mapfile.readline()
            
    def __str__(self):
        '''(world) -> string'''
        #This function is called whenever someone tries to print an object of type world
        i = 0
        while i<MAP_SIZE:
            k = 0
            while k<MAP_SIZE:
                #print(self.map[i][k],end='')
                k+=1
            print()
            i+=1
        return ''

    def _clear(self):
        '''(world) -> NoneType
        Fills the map with air blocks'''
        
        i = 0
        while i<MAP_SIZE:
            k = 0
            while k<MAP_SIZE:
                self.map[i][k] = tile()
                self.torches = []
                k+=1
            i+=1

    def depower(self):
        '''(world) -> NoneType
        Since "resolve" change the type of the tiles by adding a "*" to show that they are powered, we have to remove the star and shut the power down'''
        i = 0
        while i<MAP_SIZE:
            k = 0
            while k<MAP_SIZE:
                self.map[i][k].depower()
                k+=1
            i+=1

    def change(self,x,y,to):
        '''(world,int,int,string) -> NoneType'''
        if self.map[x][y].type == "T":
            if (x,y) in self.torches:
                self.torches.remove((x,y))
        if to=="A":
            self.map[x][y] = tile()
        elif to=="B":
            self.map[x][y] = block()
        elif to=="T":
            self.map[x][y] = torch()
            self.torches.append((x,y))
            way = ["w","a","s","d",""]
            direction = ' '
            while not direction in way:
                box=wx.TextEntryDialog(None,str(way),"On Block?","")
                if box.ShowModal()==wx.ID_OK:
                    direction=box.GetValue()
            if direction == "w":
                temp = (x-1,y)
            elif direction == "a":
                temp = (x,y-1)
            elif direction == "s":
                temp = (x+1,y)
            elif direction == "d":
                temp = (x,y+1)
            else:
                return
            if self.map[temp[0]][temp[1]].type == "B":
                self.map[x][y].onbox = direction
                self.map[x][y].box = self.map[temp[0]][temp[1]]
        elif to=="R":
            self.map[x][y] = redstone()
        elif to=="P":
            direction = ""
            way = ["w","a","s","d"]
            if ((x==MAP_SIZE-1 and y==MAP_SIZE-1) or (x==0 and y==0) or (x==0 and y==MAP_SIZE-1) or (x==MAP_SIZE-1 and y==0)):
                print ("Can't place repeater there")
                return
            if (y==MAP_SIZE-1 or y==0):
                way = ["w","s"]
            elif (x==0 or x==MAP_SIZE-1):
                way = ["a","d"]
            while not direction in way:
                box=wx.TextEntryDialog(None,str(way),"Facing?",way[0])
                if box.ShowModal()==wx.ID_OK:
                    direction=box.GetValue()
            if direction == "w":
                temp = (x-1,y)
                temp2 = (x+1,y)
            elif direction == "a":
                temp = (x,y-1)
                temp2 = (x,y+1)
            elif direction == "s":
                temp = (x+1,y)
                temp2 = (x-1,y)
            elif direction == "d":
                temp = (x,y+1)
                temp2 = (x,y-1)
            self.map[x][y] = repeater(temp,temp2)

    def show(self):
        i = 0
        while i<MAP_SIZE:
            k = 0
            while k<MAP_SIZE:
                temp = str(self.map[i][k])
                if self.map[i][k].pwr:
                    temp += "*"
                #print(temp,end='')
                k+=1
            print()
            i+=1
        print()
        print()
        return

if __name__=="__main__":
    w = world("NEW")
    print(w)
    w.change(1,1,"B")
    print(w)

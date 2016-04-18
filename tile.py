#Max redstone signal range
MAX_RANGE = 5
#For all classes self.pwr is a boolean which is True when signal is flowing through the tile.
#Types of tiles are:
# 1) Air --> Empty Space, non-conductive, Represented by an "A".
# 2) Redstone --> Redstone wire, conductive, Cost for signal to run through it is one, Represented by an "R".
# 3) Torch --> Redstone torch, the only source of redstone signal, non-conductive (power can't go THROUGH it), Represented by a "T".
# 4) Block --> Simple Block, conductive only when connected to powered repeater, Represented by a "B".
# 5) Repeater --> Redstone repeater, has a signal entrance and exit, one-way conductive (entrance to exit),
#    has a 0.1-0.5sec delay (not implemented as there is no time-keeping), Represented by a "P".
# / ---> denotes or
class tile():
    '''Parent class for every 1x1 block'''
    
    def __init__(self, typ = "A"):
        '''Make the type of the block global'''
        self.type = typ
        self.pwr = False

    def __str__(self):
        '''Return the type of the block whenever print( a-tile/child-in-here ) is called'''
        return repr(self.type)

    def _clear(self):
        ''' Clear a tile by making it an Air block'''
        self.type = "A"
        self.pwr = False

    def depower(self):
        self.type = "A"
        self.pwr = False
        
    def image(self):
        return "air.bmp"
    
class block(tile):
    
    def __init__(self):
        self.type = "B"
        self.range = 100
        self.pwr = False
        self.ton = False

    def depower(self):
        self.type = "B"
        self.pwr = False
        self.ton = False
        self.range = 100

    def image(self):
        if self.pwr:
            return "pblock.bmp"
        return "block.bmp"

class torch(tile):

    def __init__(self):
        self.pwr = True
        self.type = "T"
        self.onbox = ''
        self.box = None

    def depower(self):
        self.type = "T"
        self.pwr = True

    def image(self):
        if self.pwr:
            return "ptorch.bmp"
        return "torch.bmp"
    
class redstone(tile):

    def __init__(self):
        self.range = 100
        self.type = "R"
        self.pwr = False

    def depower(self):
        self.type = "R"
        self.pwr = False
        self.range = 100

    def image(self):
        if self.pwr:
            return "predstone.bmp"
        return "redstone.bmp"

class repeater(tile):

    def __init__(self,facing,pfrom):
        '''(repeater,tuple,tuple) --> NoneType
        Contructor of a repeater
        self.facing is a tuple (e.g. (x,y) ) with the coordinates of the tile the repeater is GIVING signal to(the EXIT)
        self.pfrom is a tuple with the coordinates of the tile the repeater is GETTING power from (the Entrance)'''
        
        self.type = "P"
        self.facing = facing
        self.pfrom = pfrom
        self.pwr = False
        
    def depower(self):
        self.type = "P"
        self.pwr = False

    def __str__(self):
        if self.facing[0]>self.pfrom[0]:
            return "v"
        elif self.facing[0]<self.pfrom[0]:
            return "^"
        elif self.facing[1]>self.pfrom[1]:
            return ">"
        else:
            return "<"

    def image(self):
        if self.facing[0]>self.pfrom[0]:
            if self.pwr:
                return "prepeaters.bmp"
            return "repeaters.bmp"
        elif self.facing[0]<self.pfrom[0]:
            if self.pwr:
                return "prepeaterw.bmp"
            return "repeaterw.bmp"
        elif self.facing[1]>self.pfrom[1]:
            if self.pwr:
                return "prepeaterd.bmp"
            return "repeaterd.bmp"
        else:
            if self.pwr:
                return "prepeatera.bmp"
            return "repeatera.bmp"


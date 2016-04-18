import wx
import os
from simulator import *

ROWS = 7
COLLUMNS = 7
class frame(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"RedStone Simulator",size = (1000,700))
        self.s = sim("7x7")
        self.panel = wx.Panel(self)
        self.buttons = []
        for x in range(ROWS):
            self.buttons.append([])
            for y in range(COLLUMNS):
                self.buttons[x].append(0)
        self.show()

    def show(self):
        panel= self.panel
        #The "Simulate" Button
        button=wx.Button(panel,label="Simulate",pos=(10,10),size=(100,60))
        self.Bind(wx.EVT_BUTTON,self.resolve,button)
        #The "Exit" Button
        button=wx.Button(panel,label="Exit",pos=(850,10),size=(100,60))
        self.Bind(wx.EVT_BUTTON,self.closebutton,button)
        
        for x in range(ROWS):
            for y in range(COLLUMNS):
                pic=wx.Image("images/"+self.s.w.map[x][y].image(),wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                self.buttons[x][y]=wx.BitmapButton(panel,-1,pic,pos=(y*85+150,x*85 + 65))
                self.buttons[x][y].x = x
                self.buttons[x][y].y = y
                self.Bind(wx.EVT_BUTTON,lambda event: self.change(event),self.buttons[x][y])

    def change(self,event):
        button = event.GetEventObject()
        box=wx.TextEntryDialog(None,"A/B/R/P/T","Change to what?","A")
        if box.ShowModal()==wx.ID_OK:
            change=box.GetValue()
        else:
            return
        self.s.w.change(button.x,button.y,str(change))
        self.resolve()
        
    def closebutton(self,event):
        self.Close(True)

    def destroy(self):
        for x in range(ROWS):
            for y in range(COLLUMNS):
                self.buttons[x][y].Destroy()

    def resolve(self,event=None):
        self.s.w.depower()
        self._resolve()
        
    def _resolve(self):
        for i in self.s.w.torches:
            x = i[0]
            y = i[1]
            if self.s.w.map[x][y].pwr:
                onblock = None
                if self.s.w.map[x][y].onbox == 'a':
                    onblock = (x,y-1)
                elif self.s.w.map[x][y].onbox == 's':
                    onblock = (x+1,y)
                elif self.s.w.map[x][y].onbox == 'd':
                    onblock = (x,y+1)
                elif self.s.w.map[x][y].onbox == 'w':
                    onblock = (x-1,y)
                if not onblock is None:
                    if self.s.w.map[onblock[0]][onblock[1]].pwr == True:
                        self.s.w.map[i[0]][i[1]].pwr = False
                    else:
                        self.s.resolve(i,1)
                else:
                    self.s.resolve(i,1)
        self.destroy()
        self.show()
        
if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=frame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()

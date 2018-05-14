from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
import random as r

Builder.load_string("""
#:kivy 1.10.0
<Board>:
    canvas:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: 310, 70
""")
class Mark(Button):
    size=(20,20)
    col=((0,0,0,0),(0.5,0.5,0.5,1),(0,0,0,1))
    val=2
    def a(self):
        self.background_color=self.col[self.val]
class Pin(Button):
    alf=1
    col = ((1, 0, 0, alf), (0, 1, 0, alf), (0, 0, 1, alf), (1, 0, 1, alf), (1, 1, 0, alf), (0, 1, 1, alf))
    val=-1
    size=(50,50)
    def on_press(self):
        if self.val+1<len(self.col):
            self.val+=1
        else:
            self.val=0
        self.background_color=self.col[self.val]
class Board(Widget):
    def Start(self):
        self.pins = list(range(4))
        for a in range(4):
            b=Pin()
            b.on_press()
            b.pos=(self.pos[0]+70+(a*60),self.pos[1]+10)
            self.add_widget(b)
            self.pins[a]=b
    def SumUp(self,resList):
        x=((self.pos[0]+10,self.pos[1]+10),(self.pos[0]+40,self.pos[1]+10),(self.pos[0]+10,self.pos[1]+40),(self.pos[0]+40,self.pos[1]+40))
        for b in range(4):
            a=Mark(pos=x[b])
            a.val=resList[b]
            a.a()
            self.add_widget(a)
class MasterMind(Widget):
    h=None
    def Test(self, inp, coder):
        out=list()
        code=list(coder)
        for a in range(4):
            if code[a]==inp[a]:
                out.append(2)
                code[a]="a"
                inp[a]=80.5
        for a in range(4):
            if code.__contains__(inp[a]):
                out.append(1)
        for a in range(4-len(out)):
            out.append(0)
        return out
    def Check(self,button):
        inp=list()
        for a in button.parent.pins:
            inp.append(a.val)
        if inp != self.code:
            button.parent.SumUp(self.Test(inp,self.code))
            button.parent.remove_widget(button) 
            if self.attempts < 5:
                self.SpawnBoard(self.attempts+1)
                self.attempts+=1
            else:
                self.EndGame(False)
                return
        else:
            self.EndGame(True)
            return       
    def SpawnBoard(self, Npos):
        a=Board()
        a.pos=(0,(self.h)-(80*Npos))
        a.Start()
        a.add_widget(Button(text="Submit",size=(50,50),pos=(a.pos[0]+10,a.pos[1]+10),on_press=self.Check))
        self.add_widget(a)
        self.b.append(a)
    def Setup(self,a=0):
        self.attempts=0
        self.b=list()
        if self.h==None:
            self.h = self.size[1]*6-70-10
        self.code=list(range(4))
        for a in range(4):
            self.code[a]=r.randint(0,5)
        self.code=tuple(self.code)
        self.SpawnBoard(0)
    def Restart(self,button):
        for a in self.b:
            self.remove_widget(a)
        self.remove_widget(self.WinLabel)
        self.remove_widget(button)
        self.Setup()
    def EndGame(self,condition):
        if condition:
            WinText = "You Won"
        else:
            WinText = "You Lost"
        self.WinLabel=Label(text=WinText,pos=(500,500),font_size=50)
        self.add_widget(self.WinLabel)
        self.add_widget(Button(text="Restart",pos=(450,470),size=(200,50),on_press=self.Restart))
class MasterMindApp(App):
    def build(self):
        game = MasterMind()
        game.Setup()
        return game

if __name__ == '__main__':
    MasterMindApp().run()
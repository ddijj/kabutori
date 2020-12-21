import random
import time

from tentoapp import *

def x():
    global kabuka,kane,motika,kabuka2,motika2,kabuka3,motika3,q
    q=int(random.randint(-10,10))
    if kabuka>0:
        kabuka=kabuka+int((q*q*q)/5)
    else:
        kabuka=100
    if kabuka2>0:
        kabuka2=kabuka2+int((q*q*q)/2)
    else:
        kabuka2=200
    if kabuka3>0:
        kabuka3=kabuka3+int((q*q*q)/1)
    else:
        kabuka3=200
    kane=kane+round(motika*kabuka*0.0005)
    kane=kane+round(motika*kabuka2*0.0005)
    kane=kane+round(motika*kabuka3*0.0005)

    a1.text=kabuka
    a2.text=kabuka2
    a3.text=kabuka3
    print("株1は"+str(kabuka))
    print("株2は"+str(kabuka2))
    print("株3は"+str(kabuka3))
    print("持ち株1は"+str(motika))
    print("持ち株2は"+str(motika2))
    print("持ち株3は"+str(motika3))
    print("残金は"+str(kane))
    app.after(1000,x)

def ko():
    global kabuka,kane,motika
    if kane>kabuka or kabuka==kane:
        kane=kane-kabuka
        motika=motika+1
        print("購入できました")
    else:
        print("購入できません")


def ur():
    global kabuka,kane,motika
    if motika>0:
        kane=kane+kabuka
        motika=motika-1
        print("購入できました")

    else:
        print("売却できません")

def ko2():
    global kabuka2,kane,motika2
    if kane>kabuka2 or kabuka2==kane:
        kane=kane-kabuka2
        motika2=motika2+1
        print("購入できました")

    else:
        print("購入できません")


def ur2():
    global kabuka2,kane,motika2
    if motika2>0:
        kane=kane+kabuka2
        motika2=motika2-1
        print("持ち株2は"+str(motika2))
        print("残金は"+str(kane))
    else:
        print("売却できません")

def ko3():
    global kabuka3,kane,motika3
    if kane>kabuka3 or kabuka3==kane:
        kane=kane-kabuka3
        motika3=motika3+1
        print("購入できました")

    else:
        print("購入できません")


def ur3():
    global kabuka3,kane,motika3
    if motika3>0:
        kane=kane+kabuka3
        motika3=motika3-1
        print("購入できました")

    else:
        print("売却できません")

kabuka=1000
motika=0
kabuka2=5000
motika2=0
kabuka3=10000
motika3=0
kane=20000
q=0

app = App()

b1 = Button(app)
b1.text = "購入"
b1.onclick=ko
b1.pack()

b2 = Button(app)
b2.text = "売却"
b2.onclick=ur
b2.pack()


a1=Label(app)
a1.text=kabuka
a1.pack()

c1 = Button(app)
c1.text = "購入"
c1.onclick=ko2
c1.pack()

c2 = Button(app)
c2.text = "売却"
c2.onclick=ur2
c2.pack()

a2=Label(app)
a2.text=kabuka2
a2.pack()

d1 = Button(app)
d1.text = "購入"
d1.onclick=ko3
d1.pack()

d2 = Button(app)
d2.text = "売却"
d2.onclick=ur3
d2.pack()

a3=Label(app)
a3.text=kabuka3
a3.pack()

app.after(1000,x)
app.start()

input()

import tkinter
import math
import numpy as np


class Satelite():
    def __init__(self, c, x=0, y=0, r=10, vx=0.25, vy=-0.5, color=(200, 200, 200)):
        self.c = c
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = "#%02x%02x%02x" % tuple(color)
        self.obj = c.create_oval(x - r, y - r, x + r, y + r, fill=self.color)
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.c.move(self.obj, self.vx, self.vy)
        
    def collision(self, x, y, R):
        if self.distance(x, y) <= self.r + R:
            self.vx *= -1.1
            self.vy *= -1.1
            
        
    def distance(self, x, y):
        return np.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


window = tkinter.Tk()
window.title('Tkinter')
window.geometry('1100x800')

c = tkinter.Canvas(width=800, height=800)
c.pack(side='right')

R = 30
r = (10, 30)
center = (400, 400)
N = 50

G = 100
M = math.pi * R ** 2

collision = True
vectors = False
time = 1

circle = c.create_oval(center[0] - R, center[1] - R, center[0] + R, center[1] + R, fill='pink')
c.pack()

def change_collision():
    global collision
    collision = not(collision)
    button_collision.config(bg=('lightgreen' if collision else 'pink'))
    
button_collision = tkinter.Button(text='Коллизия', command=change_collision, bg='lightgreen', width=27, height=2)
button_collision.place(x=5, y=240)


def change_vectors():
    global vectors
    vectors = not(vectors)
    button_vectors.config(bg=('lightgreen' if vectors else 'pink'))
    
button_vectors = tkinter.Button(text='Векторы', command=change_vectors, bg='pink', width=27, height=2)
button_vectors.place(x=5, y=290)


def change_R(event):
    global R, M, circle
    R = scale_R.get()
    M = math.pi * R ** 2
    c.delete(circle)
    circle = c.create_oval(center[0] - R, center[1] - R, center[0] + R, center[1] + R, fill='pink')
    c.pack()
    
scale_R = tkinter.Scale(window, from_=1, to=200, length=200, label='Радиус центра', orient='horizontal', command=change_R)
scale_R.set(R)
scale_R.place(x=5, y=110)


def change_N(event):
    global N
    N = scale_N.get()
    create()
    
scale_N = tkinter.Scale(window, from_=1, to=200, length=200, label='Количество', orient='horizontal', command=change_N)
scale_N.set(N)
scale_N.place(x=5, y=50)


def change_G(event):
    global G
    G = scale_G.get()
    
scale_G = tkinter.Scale(window, from_=1, to=2000, length=200, label='Сила притяжения G', orient='horizontal', command=change_G)
scale_G.set(G)
scale_G.place(x=5, y=170)


def change_time(event):
    global time
    time = scale_time.get()
    
scale_time = tkinter.Scale(window, from_=1, to=100, length=200, label='Замедление', orient='horizontal', command=change_time)
scale_time.set(time)
scale_time.place(x=5, y=350)


def reset():
    global R, N, G, M, time
    R = 30
    N = 50
    G = 100
    M = math.pi * R ** 2
    time = 1
    scale_R.set(R)
    scale_N.set(N)
    scale_G.set(G)
    scale_time.set(time)
    
button_reset = tkinter.Button(text='По умолчанию', command=reset, bg='lightgrey', width=27, height=2)
button_reset.place(x=5, y=420)


satelites = []
def create():
    global satelites
    for i in satelites:
        c.delete(i.obj)
    satelites = []
    for i in range(N):
        x = np.random.randint(100, 700)
        y = np.random.randint(100, 700)
        r_ = np.random.randint(*r)
        while np.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2) <= r_ + R:
            x = np.random.randint(100, 700)
            y = np.random.randint(100, 700)
            r_ = np.random.randint(*r)
        satelites.append(Satelite(c,
                            x=x,
                            y=y,
                            r=r_,
                            color=[np.random.randint(40, 210)] * 3,
                            vx=np.random.random() - 0.5,
                            vy=np.random.random() - 0.5))
        

button_restart = tkinter.Button(text='Пересоздать', command=create, width=27, height=2)
button_restart.place(x=5, y=5)


def update(vect):
    for i in vect:
        c.delete(i)
    vect = []
    
    for i in satelites:
        F = G * M / i.distance(*center) ** 2
        angle = np.arctan2(center[1] - i.y, center[0] - i.x)
        a = F / M
        dx, dy = a * math.cos(angle), a * math.sin(angle)
        i.vx += dx
        i.vy += dy
        i.move()
        if collision:
            i.collision(*center, R)
                
        if vectors:
            vect.append(c.create_line(i.x, i.y, i.x + 25 * i.vx, i.y + 25 * i.vy, fill='blue'))
            vect.append(c.create_line(i.x, i.y, i.x + F * math.cos(angle), i.y + F * math.sin(angle), fill='orange'))
        
    window.after(time, lambda: update(vect))

    
def main():
    create()
    update([])
    

main()
    
window.mainloop()

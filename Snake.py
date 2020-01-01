#Snake Base File

import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

class cube(object):
    roWs = 20
    w = 500
    def __init__(self, start, dirnx = -1, dirny = 0, color = (255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + dirnx, self.pos[1] + dirny)

    def draw(self, surface, eyes = False):
        #print("ASDASD{} {} {}\n".format(self.color, self.pos, self.w))
        dis = self.w//self.roWs
        
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, (255,0,0), (i*dis+1, j*dis+1, dis-1, dis-1))

        if eyes:
            center = dis//2
            radius = 3
            circleMid = (i*dis+center-radius-1, j*dis+8)
            circleMid2 = (i*dis+center+radius+3, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMid, radius)
            pygame.draw.circle(surface, (0,0,0), circleMid2, radius)


class snek(object):
    body = []
    turn = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

    def move(self):
        global flag
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()
                break

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0

                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0

                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1

                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1

                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]


        for i, x in enumerate(self.body):
            p = x.pos[:]
            if p in self.turn:
                turnd = self.turn[p]
                x.move(turnd[0], turnd[1])
                if i == len(self.body)-1:
                    self.turn.pop(p)

            else:
                if x.dirnx == -1 and x.pos[0] <= 0: x.pos = (x.roWs-1, x.pos[1])
                elif x.dirnx == 1 and x.pos[0] >= x.roWs-1: x.pos = (0, x.pos[1])
                elif x.dirny == -1 and x.pos[1] <= 0: x.pos = (x.pos[0], x.roWs-1)
                elif x.dirny == 1 and x.pos[1] >= x.roWs-1: x.pos = (x.pos[0], 0)
                else: x.move(x.dirnx, x.dirny)


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turn = {}
        self.dirnx = 0
        self.dirny = 0

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        self.body.append(cube((tail.pos[0]-dx, tail.pos[1]-dy)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, x in enumerate(self.body):
            if i == 0:
                x.draw(surface, True)
            else:
                x.draw(surface)


def drawGrid(w, row, surface):
    sizebt = w//row

    x = 0
    y = 0

    for i in range(rows):
        x += sizebt
        y += sizebt

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def redrawWin(surface):
    surface.fill((0,0,0))
    drawGrid(width, rows, surface)
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()

def randomSnack(rows, items):
    position = items.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if (len(list(filter(lambda z:z.pos==(x,y), position))))>0:
            continue
        else:
            break

    return (x,y)


def message_box(subject, content):
    root = tk.Tk()

    root.attributes("-topmost", True)

    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack, flag
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))

    s = snek((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))

    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)

        redrawWin(win)

        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print("Score: ", len(s.body))
                message_box("You Died", "Your score was: {}\n Play Again?".format(len(s.body)))

                s.reset((10,10))
                break
        




main()
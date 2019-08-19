import pygame
import time
import random
import numpy as np
import math


class Pipes:
    def __init__(self,screen,drawer,x,y,color,width,height,pipeImg):
        self.drawer = drawer
        self.color = color
        self.screen = screen
        self.x = x
        self.y =y
        self.height = height
        self.width = width
        self.pipeImg = pipeImg

    def show(self):
        #self.drawer.draw.rect(self.screen,self.color,(self.x,self.y,self.width,self.height))
        self.screen.blit(self.pipeImg,(self.x,self.y))

class Bird:
    def __init__(self,screen,drawer,radius,color,img):
        self.x = 100
        self.y = 200
        self.screen = screen
        self.drawer = drawer
        self.radius = radius
        self.color = color
        self.vel = 10
        self.accel = 1
        self.angle = 0
        self.img = img
    
    def show(self):

        self.screen.blit(self.img,(self.x-30,self.y-30))

    def jump(self):
        self.vel = -8
      
        
    
# ------- Declare Constants -------#
pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
resolution = (SCREEN_WIDTH,SCREEN_HEIGHT)
redColor = (255,0,0)
blueColor = (0,0,255)
blackColor = (0,0,0)
TITLe = "Flappy Bird Lite"
cnt = 0
win = pygame.display.set_mode(resolution)
pygame.display.set_caption(TITLe)
isRunning = True
clock = pygame.time.Clock()
xs = [500,700,900]
vel = 4
upperPipes = []
lowerPipes = []
GAP = 50
width = 60
BIRD_RADIUS = 10
 
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
base1 = pygame.image.load("./base.png")
base2 = pygame.image.load("./base.png")
background = pygame.image.load("./background-night.png")
pipeImg = pygame.image.load("./pipe-green.png")
upwing = pygame.image.load("./yellowbird-upflap.png")
midwing = pygame.image.load("./yellowbird-midflap.png")
downwing = pygame.image.load("./yellowbird-downflap.png")
wings = [upwing,midwing,downwing]
for x in xs:
    level = random.randint(100,300)
    upperPipes.append(Pipes(win,pygame,x,0,redColor,width,level-GAP,pygame.transform.rotate(pipeImg,180)))
    lowerPipes.append(Pipes(win,pygame,x,level+GAP,redColor,width,SCREEN_HEIGHT-GAP-level,pipeImg))

# screen,drawer,radius,color
bird = Bird(win,pygame,BIRD_RADIUS,blueColor,wings[1])
CNT = 0

def checkPoint(bird,upperPipes,lowerPipes):
    #print("here")
    global CNT
    for pipe in upperPipes:
        if(pipe.x+pipe.width == 0):
            continue
        if(bird.x/(pipe.x+pipe.width)==1):
            CNT+=1
            
        
            print(CNT)
        else:
            print(CNT)
            pass


def collided(bird,upperPipes,lowerPipes):
    upCollide = False
    downCollide = False
    for pipe in upperPipes:
        
        if((bird.x+BIRD_RADIUS>=pipe.x and bird.x+BIRD_RADIUS<=pipe.x+width) and bird.y-BIRD_RADIUS<=pipe.height):
            upCollide = True
            break
        else:
            upCollide = False
    for pipe in lowerPipes:
        
        if((bird.x+BIRD_RADIUS>=pipe.x and bird.x+BIRD_RADIUS<=pipe.x+width) and bird.y+BIRD_RADIUS>pipe.y):
            downCollide = True
            break
            
        else:
            downCollide = False


    return upCollide or downCollide
w_cnt = 0
base1x = 0
base2x = SCREEN_WIDTH
while isRunning:
    textsurface = myfont.render(str(CNT), False, (255, 255, 255))
    win.blit(pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT)),(0,0))
    win.blit(pygame.transform.scale(base1,(SCREEN_WIDTH+vel,base1.get_height())),(base1x,SCREEN_HEIGHT-50))
    win.blit(pygame.transform.scale(base2,(SCREEN_WIDTH+vel,base2.get_height())),(base2x,SCREEN_HEIGHT-50))
    
    level = random.randint(100,300)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            isRunning = False
    clock.tick(30)
    #time.sleep(1/30)

    for pipe in upperPipes:
        pipe.pipeImg = pygame.transform.scale(pipe.pipeImg,(pipe.width,pipe.height))
        pipe.show()
        pipe.x -=vel
        

        if(pipe.x+100 < 0):
            pipe.x = SCREEN_WIDTH
            pipe.height = level - GAP
    for pipe in lowerPipes:
        pipe.pipeImg = pygame.transform.scale(pipe.pipeImg,(pipe.width,pipe.height-50))
        pipe.show()
        pipe.x -=vel
        
        if(pipe.x+100 < 0):
            pipe.x = SCREEN_WIDTH
            pipe.y = level+GAP
            pipe.height=SCREEN_HEIGHT-GAP-level
    if(w_cnt==3):
        w_cnt=0
    bird.img = wings[w_cnt]
    
    
    
    # ------ Handling Game inputs
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_SPACE]):
        bird.y -=4
        bird.jump()
    # Y = (X-A)/(B-A) * (D-C) + C
    bird.y += bird.vel 
    if(bird.vel<0):
        bird.img = pygame.transform.rotate(wings[w_cnt],45)
    else:
        bird.img = pygame.transform.rotate(wings[w_cnt],-45)
    bird.show()
    w_cnt+=1
    
    bird.vel += bird.accel
    if(bird.vel>15):
        bird.vel=15

    if(bird.y+BIRD_RADIUS>=SCREEN_HEIGHT-70):
        bird.y = SCREEN_HEIGHT-70
    win.blit(textsurface,(245,100))
    pygame.display.update()
    base1x-=vel
    base2x-=vel
    if((base1x+SCREEN_WIDTH)<0):
        base1x = SCREEN_WIDTH
    if((base2x+SCREEN_WIDTH)<0):
        base2x = SCREEN_WIDTH
    win.fill(blackColor)
    
    if(collided(bird,upperPipes,lowerPipes)):
        
        break
        if(bird.vel > 0):
            bird.vel-=1
            vel = 0
        else:
            vel = 0
            bird.x = 100
            bird.vel = 0
            bird.accel = 0
        
    checkPoint(bird,upperPipes,lowerPipes)
    

pygame.quit()


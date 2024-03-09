from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
import math 
import pygame.math
from pygame.locals import *
import os
from math import sin, cos, pi, radians
from sys import exit as _exit
import sys
def lerp(a: float, b: float, t: float) -> float:
   
    return (1 - t) * a + t * b

def angle_lerp(a0, a1, t):
    max_angle = 360.0
    angle = ((a1 - a0 + max_angle + 180.0) % max_angle) - 180.0
    return a0 + angle * t

def rotate_triangle(center, scale, mouse_pos):

    vMouse  = pygame.math.Vector2(mouse_pos)
    vCenter = pygame.math.Vector2(center)
    angle   = pygame.math.Vector2().angle_to(vMouse - vCenter)

    points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]
    rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in points]

    triangle_points = [(vCenter + p*scale) for p in rotated_point]
    return triangle_points

def rotate_triangle_ang(center, scale, angle):
    vCenter = pygame.math.Vector2(center)
    angle   = angle

    points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]
    rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in points]

    triangle_points = [(vCenter + p*scale) for p in rotated_point]
    return triangle_points

pygame.init()
pygame.display.set_caption("Wave")
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
running = True
deltaTime = 0.0


playerPos = pygame.Vector2(0,0)
center = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
sAngle = 0.0

spawnTimer = 0.0
gameTimer = 0.0

enemies = [pygame.Vector2(screen.get_width()/4,screen.get_height()/4)]
directions = [pygame.Vector2(-1,-1)]
lifetime = [0]
id = [0]
cId = 0

pdirection = pygame.Vector2(0,0)
trails = [pygame.Vector2(screen.get_width(),0)]
trailTime = 0.0
px= center.x
py = center.y

score = 0.0
highscore = 0.0

speed = 400.0

respawnTimer = -1.0

velocity = pygame.Vector2(0,0)

DEBUG_HITBOX = False

boostTimer = 2.0

canBoost = True
invulnerable = False

light = pygame.Vector2(0,6)
maxShadowIter = 6

pygame.font.init() 

font = pygame.font.SysFont('Verdana', 30)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

hsfile = open(__location__+"/highscore.txt","w")
if hsfile.readable():
    readscore = hsfile.read()
    if len(readscore)>0:
        highscore = float(readscore)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("white")

    mouse_position = pygame.mouse.get_pos()
   
    
    px = pygame.math.lerp(px,center.x+velocity.x*5,min(deltaTime*6,1))
    py = pygame.math.lerp(py,center.y+velocity.y*5,min(deltaTime*6,1))
    pSize = 8
    playerRect = Rect(px-pSize/2,py-pSize/2,pSize,pSize)

    if velocity.x!=0 or velocity.y!=0:
        pdirection = (center.x-velocity.x*100,center.y-velocity.y*100)
        sAngle = angle_lerp(sAngle,angle,deltaTime*20  )
    for z in trails:
        e = trails.index(z)
        pygame.draw.circle(screen,pygame.color.Color(255-e*4,255-e*4,255-e*4,255),z-playerPos,4)
    angle = pygame.Vector2.angle_to(pygame.Vector2(0,0),-velocity*100)
   
    points = rotate_triangle_ang((px,py), 8, sAngle)
    
    oldPos = pygame.Vector2(playerPos.x,playerPos.y)
    if respawnTimer<=0: 
        color = pygame.color.Color(0,0,0,255)
        shadowColor = pygame.color.Color(65,65,110,255)
        if invulnerable:
            color.r = 127
            color.a= 2
        elif canBoost and boostTimer>=1:
            color.b = 255
            shadowColor.b = 255

        shadowIter = 0
        while shadowIter<maxShadowIter:
            shadowIter+=1
            pShadow = rotate_triangle_ang((px,py)+light*shadowIter/maxShadowIter, 8, sAngle)
            pygame.draw.polygon(screen,shadowColor, pShadow) 
        
        pygame.draw.polygon(screen, color, points)    
        score+=deltaTime*763
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
           playerPos.y -= speed * deltaTime
        if keys[pygame.K_s]:
            playerPos.y += speed * deltaTime
        if keys[pygame.K_a]:
            playerPos.x -= speed * deltaTime
        if keys[pygame.K_d]:    
            playerPos.x += speed * deltaTime
        if keys[pygame.K_SPACE] and len(velocity)!=0 and canBoost and boostTimer>=1:    
            speed*=8
            canBoost = False
            invulnerable = True
            boostTimer=0
    else:
        resText = font.render(str(int(respawnTimer*10)/10), False, (0,0,0))
        screen.blit(resText,(center.x-18,center.y+5))
        respawnTimer-=deltaTime
        pygame.draw.circle(screen, "black", center, (respawnTimer)*16)
    if boostTimer>=0.05 and canBoost==False:
        speed/=8
        canBoost = True
    if boostTimer>=0.25 and invulnerable:
        invulnerable=False
    boostTimer+=deltaTime

    if trailTime<=0:
        trails.append((playerPos.x+px,playerPos.y+py))
        trailTime=0.01
    trailTime-=deltaTime

    velocity = (oldPos-playerPos)
    keysDown = pygame.key.get_focused()
    

    if len(trails)>64:
        trails.pop(0)


    if DEBUG_HITBOX:
        pygame.draw.rect(screen,"cyan",playerRect)
        
    for x in enemies:
     
        i = enemies.index(x)
        x+=directions[i]*deltaTime*12
        directions[i].x+=math.sin(id[i]*0.6+gameTimer)*50*deltaTime
        directions[i].y+=math.cos(id[i]*0.8+gameTimer)*50*deltaTime
        lifetime[i]+=deltaTime 
        epos = x-playerPos
        escale =max(0,2+math.sin(math.radians((lifetime[i]/5)*360))*16)*2
        enemyRect = Rect(epos.x-escale/2,epos.y-escale/2,escale,escale)
        collide = pygame.Rect.colliderect(playerRect,enemyRect)
        
        if DEBUG_HITBOX:
            pygame.draw.rect(screen, "yellow", enemyRect)
        if collide and respawnTimer<=0 and escale > 6 and invulnerable==False:
            respawnTimer = 1
            if score>=highscore:
                hsfile = open(__location__+"/highscore.txt","w")
                hsfile.write(str(highscore))
                hsfile.close()
            score = 0
        shadowIter=0
        while shadowIter<maxShadowIter:
            shadowIter+=1
            pygame.draw.circle(screen,pygame.color.Color(160,65,65,255),(epos.x,epos.y)+light*shadowIter/maxShadowIter,escale*0.6)
        
        pygame.draw.circle(screen,"red",epos,escale*0.6)
        points = rotate_triangle((epos.x,epos.y)+directions[i].normalize()*escale*0.7, escale/8, epos+directions[i]*100)
        pygame.draw.polygon(screen, "darkred", points)   
        if lifetime[i]>5:
            directions.pop(i)
            lifetime.pop(i)
            id.pop(i)
            enemies.pop(i)


  

    deltaTime = clock.tick(144) / 1000   

 
    spawnTimer+=deltaTime
    gameTimer+=deltaTime
 
    if spawnTimer>0.05:
        spawnTimer=0
        pos = playerPos+center+pygame.Vector2(screen.get_width()/2.5*([-1,1][random.randrange(2)]),screen.get_height()/2.5*([-1,1][random.randrange(2)]))-velocity*15
        enemies.append(pos)
        npos = pos
        if pos.length()>0:
            npos = pos.normalize()
        directions.append(npos*-1)
        lifetime.append(0)
        id.append(cId)
        cId+=1
    
    if score>highscore:
        highscore=score
    scoreLabel = font.render('score', False, (0,0,0))
    screen.blit(scoreLabel,(16,16))
    scoreTxt = font.render(str(int(score)), False, (0,0,0))
    screen.blit(scoreTxt,(16,40))

    hscoreLabel = font.render('highscore', False, (0,0,0))
    screen.blit(hscoreLabel,(16,70))
    hscoreTxt = font.render(str(int(highscore)), False, (0,0,0))
    screen.blit(hscoreTxt,(16,100))
    pygame.display.flip()

pygame.quit()


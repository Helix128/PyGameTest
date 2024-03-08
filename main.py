import pygame
import random
import math 
import pygame.math
from pygame.locals import *

import pygame
from math import sin, cos, pi, radians
from sys import exit as _exit

def rotate_triangle(center, scale, mouse_pos):

    vMouse  = pygame.math.Vector2(mouse_pos)
    vCenter = pygame.math.Vector2(center)
    angle   = pygame.math.Vector2().angle_to(vMouse - vCenter)

    points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]
    rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in points]

    triangle_points = [(vCenter + p*scale) for p in rotated_point]
    return triangle_points


pygame.init()
pygame.display.set_caption("WaveFlux")
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True
deltaTime = 0


playerPos = pygame.Vector2(0,0)
center = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)

spawnTimer = 0
gameTimer = 0

enemies = [pygame.Vector2(screen.get_width()/4,screen.get_height()/4)]
directions = [pygame.Vector2(-1,-1)]
lifetime = [0]
id = [0]
cId = 0

pdirection = pygame.Vector2(0,0)
trails = [pygame.Vector2(screen.get_width(),0)]

px= center.x
py = center.y


speed = 400

respawnTimer = -1

velocity = pygame.Vector2(0,0)

DEBUG_HITBOX = False

boostTimer = 2

canBoost = True
invulnerable = False

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("gray")
    mouse_position = pygame.mouse.get_pos()
   
    
    px = pygame.math.lerp(px,center.x+velocity.x*3,min(deltaTime*5,1))
    py = pygame.math.lerp(py,center.y+velocity.y*3,min(deltaTime*5,1))
    pSize = 8
    playerRect = Rect(px-pSize/2,py-pSize/2,pSize,pSize)

    if velocity.x!=0 or velocity.y!=0:
        pdirection = (center.x-velocity.x*100,center.y-velocity.y*100)
    for z in trails:
        e = trails.index(z)
        pygame.draw.circle(screen,pygame.color.Color(0,0,0,10),z-playerPos,(64-(64-e))/12)
        
    points = rotate_triangle((px,py), 8, pdirection)
    oldPos = pygame.Vector2(playerPos.x,playerPos.y)
    if respawnTimer<=0:
        color = pygame.color.Color(0,0,0,255)
        if invulnerable:
            color.r = 127
            color.a= 2
        elif canBoost and boostTimer>=1:
            color.b = 255
        pygame.draw.polygon(screen, color, points)    
      
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
        respawnTimer-=deltaTime
        pygame.draw.circle(screen, "green", center, 16-respawnTimer*16)
    if boostTimer>=0.05 and canBoost==False:
        speed/=8
        canBoost = True
    if boostTimer>=0.25 and invulnerable:
        invulnerable=False
    boostTimer+=deltaTime
    print(boostTimer)
   
    trails.append((playerPos.x+px,playerPos.y+py))


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
        escale =max(0,2+math.sin(math.radians((lifetime[i]/3)*360))*16)*2
        enemyRect = Rect(epos.x-escale/2,epos.y-escale/2,escale,escale)
        collide = pygame.Rect.colliderect(playerRect,enemyRect)
       
        if DEBUG_HITBOX:
            pygame.draw.rect(screen, "yellow", enemyRect)
        if collide and respawnTimer<=0 and escale > 6 and invulnerable==False:
            respawnTimer = 1

        pygame.draw.circle(screen,"red",epos,escale*0.6)
        if lifetime[i]>3:
            directions.pop(i)
            lifetime.pop(i)
            id.pop(i)
            enemies.pop(i)


    pygame.display.flip()

    deltaTime = clock.tick(144) / 1000

    print(velocity/deltaTime)
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

pygame.quit()


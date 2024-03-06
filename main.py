import pygame
import random
import math 

pygame.init()
screen = pygame.display.set_mode((1280, 720))
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

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill("gray")

    pygame.draw.circle(screen,"blue",center,16)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerPos.y -= 300 * deltaTime
    if keys[pygame.K_s]:
        playerPos.y += 300 * deltaTime
    if keys[pygame.K_a]:
        playerPos.x -= 300 * deltaTime
    if keys[pygame.K_d]:    
        playerPos.x += 300 * deltaTime


    for x in enemies:
        i = enemies.index(x)
        x+=directions[i]*deltaTime
        directions[i].x+=math.sin(id[i]*0.23+gameTimer)*3
        directions[i].y+=math.cos(id[i]*0.23+gameTimer)*3
        lifetime[i]+=deltaTime 
        pygame.draw.circle(screen,"red",x-playerPos,8+math.sin(math.radians((lifetime[i]/10)*180))*32)
        if lifetime[i]>10:
            directions.pop(i)
            lifetime.pop(i)
            id.pop(i)
            enemies.pop(i)


    pygame.display.flip()

    deltaTime = clock.tick(60) / 1000
    spawnTimer+=deltaTime
    gameTimer+=deltaTime

    if spawnTimer>1:
        spawnTimer=0
        enemies.append(playerPos+center+pygame.Vector2(random.randrange(120,160)*([-1,1][random.randrange(2)]),random.randrange(70,100)*([-1,1][random.randrange(2)])))
        directions.append(pygame.Vector2((random.random()*2-1)*512,(random.random()*2-1)*512))
        lifetime.append(0)
        id.append(0)

pygame.quit()
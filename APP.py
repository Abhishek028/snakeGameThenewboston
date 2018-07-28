import pygame
import random

x = pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

display_width, display_height = (800, 600)
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Snake')
icon = pygame.image.load("snakeHead.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

block_size = 20

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

img = pygame.image.load("snakeHead.png")

direction = "right"

def pause():
    gamePaused = True
    msg_to_screen("Game Paused", red, -40, "large")
    msg_to_screen("press c to continue or q to quit", black, 40)
    pygame.display.update()
    while(gamePaused):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    gamePaused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)

        clock.tick(10)

def score(score):
    text = smallfont.render("Score: "+str(score),True,black)
    gameDisplay.blit(text,[0,0])

def game_intro():
    intro = True

    while(intro):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        msg_to_screen("Welcome to snake",green,-100,"large")
        msg_to_screen("The more apples you eat,the longer you get",black,-30)
        msg_to_screen("The objective of the game is to eat red apples",black,0)
        msg_to_screen("If you collide with your self or boundries,you die",black,30)
        msg_to_screen("Press P to pause the game",black,60)
        msg_to_screen("Press C to play and Q to quit",black,90)
        pygame.display.update()
        clock.tick(5)
def snake(block_size,snakeList):
    if direction == "right":
        head = pygame.transform.rotate(img,270)
        gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
        gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    if direction == "up":
        head = pygame.transform.rotate(img, 0)
        gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
        gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    for xny in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [xny[0],xny[1],block_size, block_size])


def generate_apple():
    Applex = random.randrange(0, display_width - block_size, 20)
    Appley = random.randrange(0, display_height - block_size, 20)
    return (Applex, Appley)
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text,True,color)
    elif size == "medium":
        textSurface = medfont.render(text,True,color)
    elif size == "large":
        textSurface = largefont.render(text,True,color)
    return textSurface,textSurface.get_rect()



def msg_to_screen(msg, color,y_displacement=0,size = "small"):
    textSurf,textRect = text_objects(msg,color,size)
    textRect.center = (display_width/2,display_height/2+y_displacement)
    gameDisplay.blit(textSurf,textRect)


def gameLoop():
    global direction
    snakeList = []
    snakeLength = 1
    justStarted = True
    gameExit = False
    gameOver = False
    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 20
    lead_y_change = 0


    while not gameExit:
        if gameOver:
            msg_to_screen("Game Over", red, -50, size="large")
            msg_to_screen("press c to continue or q to quit", black, 50, size="medium")
            pygame.display.update()
        while gameOver:
            #gameDisplay.fill(white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        direction = "right"
                        gameLoop()
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if lead_x_change != block_size:
                        lead_x_change = -block_size
                        lead_y_change = 0
                        direction = "left"
                elif event.key == pygame.K_RIGHT:
                    if lead_x_change != -block_size:
                        lead_x_change = +block_size
                        lead_y_change = 0
                        direction = "right"
                elif event.key == pygame.K_UP:
                    if lead_y_change != block_size:
                        lead_y_change = -block_size
                        lead_x_change = 0
                        direction = "up"
                elif event.key == pygame.K_DOWN:
                    if lead_y_change != -block_size:
                        lead_y_change = block_size
                        lead_x_change = 0
                        direction = "down"
                elif event.key == pygame.K_p:
                    pause()

        lead_x += lead_x_change
        lead_y += lead_y_change
        if lead_x > display_width - 20 or lead_x < 0 or lead_y > display_height - 20 or lead_y < 0:
            gameOver = True
        gameDisplay.fill(white)
        if justStarted:
            Applex, Appley = generate_apple()
            justStarted = False
        score(snakeLength-1)

        apple = pygame.image.load("apple.png")
        #pygame.draw.rect(gameDisplay, red, [Applex, Appley, block_size, block_size])
        gameDisplay.blit(apple,(Applex,Appley))



        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
        for eachSegment in snakeList[0:len(snakeList)-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size,snakeList)
        pygame.display.update()
        clock.tick(10)

        if lead_x == Applex and lead_y == Appley:
            #print("om nom nom")
            Applex, Appley = generate_apple()
            snakeLength+=1
        #pause()

    pygame.quit()

    quit()

game_intro()
gameLoop()

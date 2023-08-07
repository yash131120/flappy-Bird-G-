import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32
SCREENWIDTH = 389
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.jpg'
PIPE = 'gallery/sprites/pipe.png'



def welcomeScreen():
    """
    Shows welcome images on the screen
    """
 
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    massagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # if the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, massagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
                
                
                # ..............55:00...........
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0     
    
    #Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    
    pipeVelX = -4
    
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY =1
    
    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the brid is flapping
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quite()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerAccY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
          
    crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
    if crashTest:
        return
    
    #check for score
    playerMinPos = playerx + GAME_SPRITES['player'].get_width()/2
    for pipe in upperPipes:
        playerMinPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
        if pipeMidPos <= playerMinPos < pipMidPos +4:
            score += 1
            print(f"Your score is {score}")
        GAME_SOUNDS['point'].play()       
    
     
    if playerVelY <playerMaxVelY and not playerFlapped:
        playerVelY += playerAccY
    
    if playerFlapped:
        playerFlapped = False
    playerHeight = GAME_SPRITES['player'].get_height()
    playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)         
    
    # move pipes to the left
    for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
        upperPipe['x'] += pipeVelX
        lowerPip['x'] += pipeVelX
        
    # Add a new pipe when the first is about to cross the leftmost part of the screen
    if 0<upperPipes[0]['x']<5:
        newpipes.append(newpipe[0])
        upperPipes.append(newPipe[0])
        lowerPipes.append(newPipe[1]) 
                        
    # if the pipe is out of the screen, remove it
    if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
        upperPipes.pop(0)
        lowerPipes.pop(0)
    
    # Lets bilt our sprites now
    SCREEN.blit(GAME_SPRITES['background'], (0, 0))
    for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
        SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipes['x'], upperPipes['y']))
        SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipes['x'], lowerPipes['y']))
        
    SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
    SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
    myDigits = [int(x) for x in list(str(score))]
    width = 0
    for digit in myDigits:
        width += GAME_SPRITES['numbers'][digit].get_width()
    Xoffset = (SCREENWIDTH - width)/2
    
    for digit in myDigits:
        SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
        Xoffset += GAME_SPRITES['numbers'][digit].get_width()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
           
           
           
def isCollide(playerx, playery, upperPipes, LowerPipes):
    return False        
def getRandomPipe():
    """
    Generate position of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """    
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENWIDTH - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1} #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe     
           
           
           
if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initializa all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by YashVavaliya')
    GAME_SPRITES['numbers'] = (
        # cheng alpha&pixal for img  convert_alpha()
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base1.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    
    #Game Sound
    #GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.mp3')
    #GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.mp3')
    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    
    while True:
        welcomeScreen() # shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function
        
    
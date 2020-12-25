
# For generating random numbers . Module in Python . It will be used for making pipes in game
import random 
# We will use sys.exit() to exit the program . If user presses cross button then the program closes.
import sys
# Basic pygame imports. Next 2 lines
import pygame
from pygame.locals import * 


# Global Variables for game

# FPS - MEANS HOW MAY FRAMES ARE RENDERING WITHIN PER SECOND. IF WE REDUCE FPS THEN THE GAME WILL LAG.
FPS = 32
# SCREENWIDTH AND SCREENHEIGHT GENERATED ON TRIAL BASIS
SCREENWIDTH = 289
SCREENHEIGHT = 511
# INITIALISE A WINDOW OR SCREEN FOR GAME (pygame.display.setmode())

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

GROUNDY = SCREENHEIGHT * 0.8 # 80 percent bhi le sakte hai
GAME_SPRITES = {}
GAME_SOUNDS = {}
# we give path by this method
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    # These are dimension so that bird comes at the center of screen
    playerx = int(SCREENWIDTH/5) # Check kiya  
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()  # IF WE WILL NOT RUN THIS , SCREEN WILL NOT BE CHANGED
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0  # BASE KA X COORDINATE .TAKEN FROM TOP LEFT CORNER

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},  # (screenwidth/2) the reason for this is .here the next random pipe will appear
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    # Now we will give velocity to each of the component.
    pipeVelX = -4  # we have to move pipe oppsite direction relative to bird

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -10 # velocity while flapping. Bird ko forward move karne ke liye otherwise the bird will move vertically only
    playerFlapped = False # Binary Variable. It is true only when the bird is flapping

    # MAIN GAME LOOP
    while True:
        for event in pygame.event.get(): # Exit Condition
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):  # event.type == keydown means user has pressed some key on keyboard
                if playery > 0:  # Means Player is inside the screen
                    playerVelY = playerFlapAccv 
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        # CHECKING THE SCORE
        # LOGIC FOR CALCULATING SCORE 
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4: # SMALL BAND OF GAP IS TAKEN
                score +=1
                print(f"Your score is {score}")  # f-string method for string formatting
                GAME_SOUNDS['point'].play()  #function for playing sounds


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped: # Suppose player pressed the upper arrow key for one time only, then that means player is not flapping . therefor playerflapped ko false kiya hai
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # MOVING PIPES TO LEFT
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:  # When this pipe is about to leave the screen . Now we have the task to get the next random pipe
            newpipe = getRandomPipe()  # Function called for generating a new random pipe
            upperPipes.append(newpipe[0])  #  new pipe generated ko add kardiya
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width(): # SEE PHOTO ATTACHED FOR A CLEAR EXPLAINATION
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Blitting the sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))] # List Comprehension . Eg. if input is 32,  then we will get list of 3 and 2
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2  # Same logic . numbers ko center mai show karne ke liye . jaise ki bird ke case mai kiya tha. here (sw - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.04))  # Value agar increase karege toh score counter neeche shift hota jayega
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()  # xoffset there is an increment because next digit jo aaye ga woh bhi kuch space lega
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():  
   
    # WILL RETURN 2 PIPE ONE IS UPPER PIPE AT [0] AND OTHER IS LOWER PIPE AT [1] 
    pipeHeight = GAME_SPRITES['pipe'][0].get_height() # YOU CAN TAKE ANY PIPE FROM THAT TUPLE BECAUSE PIPE HEIGHT WILL REMAIN SAME ONLY.
    offset = SCREENHEIGHT/3.3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe WITH SIGN
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe



# HERE IS THE MAIN POINT FROM WHERE OUR GAME STARTS AFTER DEFINING GLOBAL VARIABLES


if __name__ == "__main__": 
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()  # CLOCK IS USED TO CONTROL FPS OF THE GAME. IN GAME LOOP WHEN WE WILL WRITE for eg. clock.tick(40) means it will not take the game to more than 40 fps
    pygame.display.set_caption('Flappy Bird by Rahul Rai')  # Window par caption set ho jayga
    # IMAGES PATH WILL BE STORED IN TUPLE
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(), # CONVERT_ALPHA() IS FUNCTION WHICH HELPS RENDER IMAGES FASTER ON THE SCREEN.
        pygame.image.load('gallery/sprites/1.png').convert_alpha(), # convert_alpha() images and pixel dono ko change karta hai
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),  # convert() only plays a role in pixel change
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    # PIPE should of 2 types . this can be achieved by the rotate function
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    ) # Pygame.transform.rotate(1st arg,2nd arg) . 2nd arg is the angle for which it rotates

    # GAME SOUNDS. FORMATION OF A DICTIONARY AND USING KEY WILL HELP US . 
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha() # CONVERT AND CONVERT_ALPHA BOTH CAN BE USED . TESTED BOTH BUT THERE IS NO DIFFERENCE. 
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
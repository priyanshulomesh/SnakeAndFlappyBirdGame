#snake
import pygame
from pygame.locals import *
import time
import random
import sys
SIZE=40
Colour=(110,110,5)
class Apple:
    def __init__(self,parent_screen):
        self.apple=pygame.image.load("sprites/apple.png").convert()
        self.parent_screen=parent_screen
        self.apple_x=SIZE*5
        self.apple_y=SIZE*5
    def draw (self):
        self.parent_screen.blit(self.apple,(self.apple_x,self.apple_y))
        pygame.display.flip()
    def move(self):
        self.apple_x=random.randint(1,23)*SIZE
        self.apple_y=random.randint(1,16)*SIZE
class Snake:
    def __init__(self, parent_screen,length):
        self.length=length
        self.parent_screen=parent_screen
        self.block=pygame.image.load("sprites/block.png").convert()
        self.block_x=[SIZE]*length
        self.block_y=[SIZE]*length
        self.direction='down'

    def move_up(self):
        self.direction='up'
    def move_down(self):
        self.direction='down'
    def move_right(self):
        self.direction='right'
    def move_left(self):
        self.direction='left'

    def snake_crawl(self):
        for i in range (self.length-1,0,-1):
            self.block_x[i]=self.block_x[i-1]
            self.block_y[i]=self.block_y[i-1]
        if self.direction=='left':
            self.block_x[0]-=SIZE
        if self.direction=='right':
            self.block_x[0]+=SIZE
        if self.direction=='up':
            self.block_y[0]-=SIZE
        if self.direction=='down':
            self.block_y[0]+=SIZE
        self.draw()

    def draw(self):
        self.parent_screen.fill((110,110,5))
        for i in range (self.length):
            self.parent_screen.blit(self.block,(self.block_x[i],self.block_y[i]))
        pygame.display.flip()
    def inc_length(self):
        self.length+=1
        self.block_x.append(-1)
        self.block_y.append(-1)
   

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")
        self.surface=pygame.display.set_mode((1000,680))
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()
    def collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True
        return False
    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)
    def limit (self,x1,y1,x2,y2):
        if x1>=x2 or x1<0 or y1>=y2 or y1<0:
            return True
        return False
    def play_game(self):
        self.snake.snake_crawl()
        self.apple.draw()
        self.display_score()
        pygame.display.flip() 
        if (self.collision(self.snake.block_x[0],self.snake.block_y[0],self.apple.apple_x,self.apple.apple_y)):
            self.apple.move()
            self.snake.inc_length()
        for i in range(1,self.snake.length):
            if (self.collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.block_x[i],self.snake.block_y[i])):
                raise "Game Over"
        if (self.limit(self.snake.block_x[0],self.snake.block_y[0],1000,680)):
            raise "Game Over"
    def show_game_over(self):
        self.surface.fill(Colour)
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is over! Your score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(200,300))
        line2=font.render("To play again press Enter.To exit press Escape!",True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()    
    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"Score: {self.snake.length}", True, (200,200,200))
        self.surface.blit(score, (500,10))
    def run(self):
        running=True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        running=False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key==K_DOWN:
                            self.snake.move_down()
                        if event.key==K_UP:
                            self.snake.move_up()
                        if event.key==K_LEFT:
                            self.snake.move_left()
                        if event.key==K_RIGHT:
                            self.snake.move_right()
                elif event.type==QUIT:
                    running=False
            try:
                if not pause:
                    self.play_game()
            except Exception as e:
                self.show_game_over()
                pause=True    
                self.reset()
            time.sleep(0.3)


#flappy
#global variables
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='sprites/bird.png'
BACKGROUND='sprites/background.png'
PIPE='sprites/pipe.png'
def welcomeScreen():
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update();
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    #create 2 pipes
    newPipe1=getRandomPipe();
    newPipe2=getRandomPipe();

    #list of upper pipes
    upperPipes=[
       {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
       {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']}
    ]
    # list of lower pipes 
    lowerPipes=[
       {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
       {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']}
    ]
     
    
    pipeVelX=-4
    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=1

    playerFlapVel=-8#velocity while flapping
    playerFlapped=False

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playerVelY=playerFlapVel
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()
        
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
        
        #score
        playerMid=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMid=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMid<=playerMid<pipeMid+4:
                score+=1
                GAME_SOUNDS['point'].play()


        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+=playerAccY

        if playerFlapped:
            playerFlapped=False
        playerHeight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playerVelY,GROUNDY-playery-playerHeight)
        
        #move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX    
            lowerPipe['x']+=pipeVelX    

        #add new pipe when the= first is about to cross the leftmost part
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        #if the pipe is out of the screen,remove it
        if upperPipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits=[int(x) for x in list(str(score))]
        width =0
        for digit in myDigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
        Xoffset=(SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery>GROUNDY-25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight=GAME_SPRITES['pipe'][0].get_height()
        if(playery<pipeHeight+pipe['y'] and (abs(playerx - pipe['x'])<GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerPipes:
        if(playery+GAME_SPRITES['player'].get_height()>pipe['y'] and (abs(playerx - pipe['x'])<GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe():
     PipeHeight = GAME_SPRITES['pipe'][0].get_height()
     offset=SCREENHEIGHT/3
     y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
     pipeX=SCREENWIDTH+10
     y1=PipeHeight-y2+offset
     pipe=[
         {'x':pipeX,'y':-y1},#upper pipe
         {'x':pipeX,'y':y2}#lower pipe
     ]
     return pipe

if __name__=="__main__":
    #this is main function where game start
    a=int(input("Input 1 for flappy bird and 2 for snake and apple\n"));
    if(a==2):
        game=Game()
        game.run()
        exit()
    
    elif(a!=1):
        print("Wrong input\n")
        exit()
    pygame.init()#initialize pygame modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers']=(
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message']=pygame.image.load('sprites/message.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe']=(
    
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()


#gamesounds
GAME_SOUNDS['die']=pygame.mixer.Sound('audio/die.wav')
GAME_SOUNDS['hit']=pygame.mixer.Sound('audio/hit.wav')
GAME_SOUNDS['point']=pygame.mixer.Sound('audio/point.wav')
GAME_SOUNDS['swoosh']=pygame.mixer.Sound('audio/swoosh.wav')
GAME_SOUNDS['wing']=pygame.mixer.Sound('audio/wing.wav')

while True:
    welcomeScreen()
    mainGame()
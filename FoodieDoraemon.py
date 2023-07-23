from cvzone.FaceMeshModule import FaceMeshDetector
import cv2
import sys,time,random,pygame,os
from collections import deque
fpsClock = pygame.time.Clock()

pygame.init()
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)
screen=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
pygame.display.set_caption("Foodie Doraemon")
pygame.mixer.init()
pygame.mixer.music.load("Assests\music.mp3")
pygame.mixer.music.set_volume(1.6)
pygame.mixer.music.play(-1)

doraemon = pygame.image.load("Assests\doraemon.png")
doraemon = pygame.transform.scale(doraemon, (doraemon.get_width() / 6, doraemon.get_height() / 6))
doraemon_frame = doraemon.get_rect()
doraemon_frame.center = (1280 // 6, 720 // 2)

dcscore=pygame.image.load("Assests\dcscore.png")
dcscore=pygame.transform.scale(dcscore,(80,80))

class Pipe:
    def __init__(self,x):
        self.dc=pygame.image.load("Assests\DC.png")
        self.dc=pygame.transform.scale(self.dc,(80,80))
        self.pipe_img = pygame.image.load("Assests\pipe_sprite_single.png")
        self.pipeX=1180+x
        self.pipeY=random.randrange(200,600)
        self.pipeD=True


pipeList=[]
for i in range(0,4):
    pipeList.append(Pipe(i*300))

detector = FaceMeshDetector(maxFaces=1)
speed=5
SCORE=0
font = pygame.font.SysFont("Arial", 40)
font2=pygame.font.SysFont("Arial",130)
gameOver=False
run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            pygame.quit()
    if gameOver==True:
            frame=pygame.image.load("Assests\GameOver.png")
            frame=pygame.transform.scale(frame,(1280,720))
            screen.blit(frame,(0,0))
            result=font2.render(f"{SCORE}",True,(194,122,37))
            screen.blit(result,(800,400))
            pygame.mixer.music.pause()
    else:
            success, img = cap.read()
            _, faces = detector.findFaceMesh(img,draw=False)
            if faces:
                doraemon_frame.centery=faces[0][94][1]
            img=cv2.flip(img,1).swapaxes(0,1)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(img).convert()
            screen.blit(frame,(0,0))
            screen.blit(doraemon,doraemon_frame)
            for obj in pipeList:
                screen.blit(obj.pipe_img,(obj.pipeX,obj.pipeY))
                if obj.pipeD:
                    screen.blit(obj.dc,(obj.pipeX,obj.pipeY-105))
                if doraemon_frame.collidepoint(obj.pipeX,obj.pipeY-105) and obj.pipeD:
                    obj.pipeD=False
                    SCORE+=1
                
                for i in range(1,11):
                    if doraemon_frame.collidepoint(obj.pipeX,obj.pipeY+50*i):
                        gameOver=True
                obj.pipeX-=speed
                if obj.pipeX<0:
                    obj.pipeY=random.randint(200,600)
                    obj.pipeX=1180
                    obj.pipeD=True
            else:
                speed+=0.03
            text = font.render(f"Score:{SCORE}", True,(0,0,0))
            screen.blit(text,(20,50))
            screen.blit(dcscore,(150,30))
    pygame.display.update()
    fpsClock.tick(30)


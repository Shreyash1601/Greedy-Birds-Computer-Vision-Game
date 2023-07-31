from cvzone.FaceMeshModule import FaceMeshDetector
import cv2
import sys,time,random,pygame,os
from collections import deque
from Pipes import Pipe,PipeImages
fpsClock = pygame.time.Clock()

pygame.init()
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)
screen=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
pygame.display.set_caption("Greedy Birds")
pygame.mixer.init()
pygame.mixer.music.load("Assests\music.mp3")
pygame.mixer.music.set_volume(1.6)
pygame.mixer.music.play(-1)

birdSprite=[f"Assests\\birds\\{n}.png" for n in range(1,8)]
bird = pygame.image.load(birdSprite[0])
bird = pygame.transform.scale(bird, (bird.get_width() / 7, bird.get_height() / 7))
bird_frame = bird.get_rect()
bird_frame.center = (1280 // 6, 720 // 2)

dcscore=pygame.image.load("Assests\dcscore.png")
dcscore=pygame.transform.scale(dcscore,(80,80))


pipeList=[]
for i in range(0,4):
    pipeList.append(Pipe(i*300))

sprites=["Assests\coins\\1.png","Assests\coins\\2.png","Assests\coins\\3.png","Assests\coins\\4.png","Assests\coins\\5.png","Assests\coins\\6.png"]


detector = FaceMeshDetector(maxFaces=1)
speed=5
SCORE=0
font = pygame.font.SysFont("Arial", 40)
font2=pygame.font.SysFont("Arial",130)
gameOver=False
run=True
i=0
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
            cap.release()
            cv2.destroyAllWindows()
    else:
            doraemon = pygame.transform.scale(pygame.image.load(birdSprite[i]),(110,110))
            
            success, img = cap.read()
            _, faces = detector.findFaceMesh(img,draw=False)
            if faces:
                bird_frame.centery=faces[0][94][1]
            img=cv2.flip(img,1).swapaxes(0,1)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(img).convert()
            screen.blit(frame,(0,0))
            screen.blit(doraemon,bird_frame)
            for obj in pipeList:
                obj.update()
                screen.blit(obj.pipe_img,(obj.pipeX,obj.pipeY))
                screen.blit(obj.Ipipe_img,(obj.pipeX,obj.pipeIY))
                if obj.pipeD:
                    screen.blit(obj.dc,(obj.pipeX,obj.pipeY-105))
                if bird_frame.collidepoint(obj.pipeX,obj.pipeY-105) and obj.pipeD:
                    obj.pipeD=False
                    SCORE+=1
                
                for j in range(0,11):
                  if bird_frame.collidepoint(obj.pipeX,obj.pipeY+50*j) or bird_frame.collidepoint(obj.pipeX,950-abs(obj.pipeIY-50*j)):
                        gameOver=True
                obj.pipeX-=speed
                if obj.pipeX<0:
                    OBJ=pipeList.pop(0)
                    del OBJ
                    pipeList.append(Pipe(0))

            else:
                speed+=0.03
            text = font.render(f"Score:{SCORE}", True,(255,255,255))
            screen.blit(text,(20,50))
            screen.blit(dcscore,(150,30))
    i=(i+1)%7
    pygame.display.update()
    fpsClock.tick(30)


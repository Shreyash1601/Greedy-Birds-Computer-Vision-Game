import pygame,random,image



PipeImages=["Assests\green.png","Assests\\blue.png","Assests\yellow.png","Assests\\red.png"]



class Pipe:
    def __init__(self,x):
        self.sprites=["Assests\coins\\1.png","Assests\coins\\2.png","Assests\coins\\3.png","Assests\coins\\4.png","Assests\coins\\5.png","Assests\coins\\6.png"]
        self.index=0
        self.dc=image.load(self.sprites[self.index])
        self.dc=pygame.transform.scale(self.dc,(80,80))
        self.pipe_img = pygame.image.load(random.choice(PipeImages))
        self.Ipipe_img=pygame.transform.flip(self.pipe_img,False,True)
        self.pipeX=1180+x
        self.pipeY=random.randint(300,600)
        self.pipeIY=self.pipeY-150-1000
        self.pipeD=True
    def update(self):
        self.index=(self.index+1)%6
        self.dc=image.load(self.sprites[self.index])
        self.dc=pygame.transform.scale(self.dc,(80,80))

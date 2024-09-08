import pygame
import cv2
import numpy as np

pygame.init()

width,height=1280,720
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("my game")

fps=30
clock= pygame.time.Clock()

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

start=True
while start:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            start=False
            pygame.quit()
    
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB=np.rot90(img)
    frame=pygame.surfarray.make_surface(imgRGB).convert()
    window.blit(frame,(0,0))

    pygame.display.update()

    clock.tick(fps)
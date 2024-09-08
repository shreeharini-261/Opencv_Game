import pygame

pygame.init()

width,height=1280,720
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("my game")

fps=30
clock= pygame.time.Clock()

imgbackground=pygame.image.load('/home/shree-xd/Documents/CVgameclub/resources/Nerko_One/drago.png').convert()
imgtranparent=pygame.image.load("/home/shree-xd/Documents/CVgameclub/resources/Nerko_One/watercolorbutterfly.png").convert_alpha()
imgtranparent=pygame.transform.rotate(imgtranparent,60)
imgtranparent=pygame.transform.flip(imgtranparent,True,False)
#imgtranparent= pygame.transform.scale(imgtranparent,(417,310))
imgtranparent= pygame.transform.smoothscale(imgtranparent,(417,310))
rectbutterfly= imgtranparent.get_rect()
#Rect
rectNew= pygame.Rect(500,0,200,200)

start=True
while start:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            start=False
            pygame.quit()
    
    print(rectbutterfly.colliderect(rectNew))
    rectbutterfly.x+=2 #makes it move

    window.fill((255, 255, 255))
    #pygame.draw.rect(window, (0,255,0), rectbutterfly)
    #pygame.draw.rect(window, (0,255,0), rectNew)
    #window.blit(imgbackground, (100,100))
    window.blit(imgtranparent, rectbutterfly)

    pygame.display.update()

    clock.tick(fps)
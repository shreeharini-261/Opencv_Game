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

start=True
while start:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            start=False
            pygame.quit()
    
    window.fill((255, 255, 255))
    #window.blit(imgbackground, (100,100))
    window.blit(imgtranparent, (100,100))

    pygame.display.update()

    clock.tick(fps)
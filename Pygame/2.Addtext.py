import pygame

pygame.init()

width,height=1280,720
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("my game")

fps=30
clock= pygame.time.Clock()

start=True
while start:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            start=False
            pygame.quit()
    
    window.fill((0, 0, 0))
    font=pygame.font.Font('/home/shree-xd/Documents/CVgameclub/resources/Nerko_One/NerkoOne-Regular.ttf' ,100)
    text=font.render("My Game", True,(50,50,50))
    window.blit(text, (350,300))

    pygame.display.update()

    clock.tick(fps)
""" 
pygame template
import
initialize
create window
initialize the clock for FPS
loop 
    get events
    if quit
        quit game
    apply logic
    update display/window
    set FPS
"""

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

    pygame.display.update()

    clock.tick(fps)
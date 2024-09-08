import pygame
import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import json

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("GAME")

fps = 30
clock = pygame.time.Clock()
speed = 25
score = 0
game_duration = 30 * 1000  

detector = HandDetector(detectionCon=0.8, maxHands=1)

def resetbutterfly():
    rectbutterfly.x = random.randint(100, width - 100)
    rectbutterfly.y = height + 50



cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgbutterfly = pygame.image.load("/home/shree-xd/Documents/CVgameclub/resources/Nerko_One/watercolorbutterfly.png").convert_alpha()
imgbutterfly = pygame.transform.smoothscale(imgbutterfly, (206, 155))
rectbutterfly = imgbutterfly.get_rect()
rectbutterfly.x, rectbutterfly.y = 500, 300

start = True
start_time = pygame.time.get_ticks()  #start time

while start:
    # Check if 30 seconds have passed
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= game_duration:
        start = False
        print(f"Game Over! Final Score: {score}")
        font = pygame.font.Font('/home/shree-xd/Documents/CVgameclub/resources/Nerko_One/NerkoOne-Regular.ttf', 100)
        textFinal = font.render(f'Final Score: {score}', True, (255, 50, 50))
        window.blit(textFinal, (width // 3, height // 2))
        pygame.display.update()
        pygame.time.delay(5000)  
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
    
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    rectbutterfly.y -= speed

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame=pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))

    if rectbutterfly.y < 0:
        resetbutterfly()
        speed += 1
    
    window.blit(imgbutterfly, rectbutterfly)

    if hands:
        hand = hands[0]
        x, y, _ = hand['lmList'][8]
        y=img.shape[0]-y
        print(f"Hand: ({x}, {y}) | Butterfly: ({rectbutterfly.x}, {rectbutterfly.y})")
        if rectbutterfly.inflate(20,20).collidepoint(x, y):
            print("Collision detected!")
            resetbutterfly()
            score += 1
            speed += 5

    font = pygame.font.Font(None, 50)
    textScore = font.render(f'Score: {score}', True, (255, 50, 50))
    window.blit(textScore, (35, 35))

    # Display the remaining time
    remaining_time = max(0, (game_duration - elapsed_time) // 1000)
    textTime = font.render(f'Time: {remaining_time}s', True, (255, 50, 50))
    window.blit(textTime, (width - 200, 35))

    pygame.display.update()
    clock.tick(fps)
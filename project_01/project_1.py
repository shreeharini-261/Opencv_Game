import pygame
import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
from leaderboard_1 import load_leaderboard, save_leaderboard, update_leaderboard  

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

def display_leaderboard(window, width, height):
    leaderboard = load_leaderboard()
    
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)
    
    window.fill((0, 0, 0))
    
    title_text = font.render('Leaderboard', True, (255, 255, 255))
    window.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))
    
    for i, entry in enumerate(leaderboard):
        score_text = small_font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
        window.blit(score_text, (width // 2 - score_text.get_width() // 2, 150 + i * 50))
    
    name_prompt = small_font.render('Enter your name: ', True, (255, 255, 255))
    window.blit(name_prompt, (width // 2 - name_prompt.get_width() // 2, 350))
    
    pygame.display.update()

    player_name = ''
    entering_name = True
    while entering_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to submit name
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        
        # Redraw input text box
        window.fill((0, 0, 0), (width // 2 - 200, 400, 400, 50))  # Clear previous text
        name_input = small_font.render(player_name, True, (255, 255, 255))
        window.blit(name_input, (width // 2 - name_input.get_width() // 2, 400))
        pygame.display.update()

    return player_name

player_name = display_leaderboard(window, width, height)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgbutterfly = pygame.image.load("/home/shree-xd/Documents/CVgameclub/resources/Nerko_One/watercolorbutterfly.png").convert_alpha()
imgbutterfly = pygame.transform.smoothscale(imgbutterfly, (206, 155))
rectbutterfly = imgbutterfly.get_rect()
rectbutterfly.x, rectbutterfly.y = 500, 300

def resetbutterfly():
    rectbutterfly.x = random.randint(100, width - 100)
    rectbutterfly.y = height + 50

start = True
start_time = pygame.time.get_ticks() 

while start:
    
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= game_duration:
        start = False
        print(f"Game Over! Final Score: {score}")
        
        leaderboard = load_leaderboard()
        update_leaderboard(leaderboard, player_name, score)
        
        font = pygame.font.Font(None, 100)
        window.fill((0, 0, 0))  # Clear screen
        textFinal = font.render(f'Final Score: {score}', True, (255, 50, 50))
        window.blit(textFinal, (width // 3, height // 2))
        pygame.display.update()
        
        pygame.time.wait(5000)  

        pygame.quit()
        exit()  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
            exit()

    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)
    rectbutterfly.y -= speed

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))

    if rectbutterfly.y < 0:
        resetbutterfly()
        speed += 1
    
    window.blit(imgbutterfly, rectbutterfly)

    if hands:
        hand = hands[0]
        x, y, _ = hand['lmList'][8]
        print(f"Hand: ({x}, {y}) | Butterfly: ({rectbutterfly.x}, {rectbutterfly.y})")
        if rectbutterfly.inflate(20,20).collidepoint(x, y):
            print("Collision detected!")
            resetbutterfly()
            score += 1
            speed += 5

    font = pygame.font.Font(None, 50)
    textScore = font.render(f'Score: {score}', True, (255, 50, 50))
    window.blit(textScore, (35, 35))

    remaining_time = max(0, (game_duration - elapsed_time) // 1000)
    textTime = font.render(f'Time: {remaining_time}s', True, (255, 50, 50))
    window.blit(textTime, (width - 200, 35))

    pygame.display.update()
    clock.tick(fps)

import pygame
import cv2
import random
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import json
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Piano Tiles with Gesture Controls")

# Game Variables
fps = 30
clock = pygame.time.Clock()
tile_speed = 5  # Speed of tile movement
tile_interval = 2000  # Interval to add new tiles (milliseconds)
last_tile_time = pygame.time.get_ticks()
score = 0
game_duration = 30 * 1000  # 30 seconds in milliseconds
font = pygame.font.Font(None, 50)

# Leaderboard File
leaderboard_file = 'leaderboard.json'

# Load leaderboard data
def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as f:
            return json.load(f)
    else:
        return [{"name": "", "score": 0} for _ in range(3)]

# Save leaderboard data
def save_leaderboard(leaderboard):
    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f)

# Update leaderboard if the new score is in the top three
def update_leaderboard(new_score):
    leaderboard = load_leaderboard()
    for i, entry in enumerate(leaderboard):
        if new_score > entry["score"]:
            name = input("New High Score! Enter your name: ")
            leaderboard.insert(i, {"name": name, "score": new_score})
            leaderboard = leaderboard[:3]  # Keep only top three scores
            save_leaderboard(leaderboard)
            break

# Display leaderboard
def display_leaderboard(window):
    leaderboard = load_leaderboard()
    font = pygame.font.Font(None, 50)
    y_offset = 100
    for i, entry in enumerate(leaderboard):
        text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
        window.blit(text, (width // 2 - 200, y_offset + i * 60))

# Initialize Camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Game Loop Control
start = True
start_time = pygame.time.get_ticks()

# Lane Configuration
lanes = [width // 4 * i + width // 8 for i in range(4)]  # 4 lanes
tiles = []  # List to store tiles

# Function to create new tiles
def create_tile():
    lane = random.choice(lanes)
    rect = pygame.Rect(lane - 50, 0, 100, 100)  # Create tile rectangle
    tiles.append(rect)

# Detect "taps" on tiles
def detect_tap(hand, tiles):
    x, y, _ = hand['lmList'][8]  # Index finger tip coordinates
    for tile in tiles:
        if tile.collidepoint(x, y):  # If finger tip collides with tile
            tiles.remove(tile)
            return True
    return False

# Main Game Loop
while start:
    # Check if 30 seconds have passed
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= game_duration:
        start = False
        print(f"Game Over! Final Score: {score}")
        update_leaderboard(score)
        display_leaderboard(window)
        pygame.display.update()
        pygame.time.delay(5000)  # Display the final leaderboard for 5 seconds
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
    
    success, img = cap.read()
    
    # Flip the webcam feed horizontally for a mirrored effect
    img = cv2.flip(img, 1)

    # Hand detection with cvzone
    hands, img = detector.findHands(img)

    # Check time to add new tile
    if pygame.time.get_ticks() - last_tile_time > tile_interval:
        create_tile()
        last_tile_time = pygame.time.get_ticks()

    # Move tiles down the screen
    for tile in tiles:
        tile.y += tile_speed
        if tile.y > height:  # If tile goes past screen
            # Game over condition or remove tile
            tiles.remove(tile)

    # Detect gestures and "tap" tiles
    if hands:
        hand = hands[0]
        if detect_tap(hand, tiles):
            score += 1  # Increase score on successful tap
            tile_speed += 0.2  # Increase speed slightly with each tap

    # Convert BGR image to RGB and rotate for Pygame display
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    
    window.blit(frame, (0, 0))

    # Render tiles
    for tile in tiles:
        pygame.draw.rect(window, (255, 0, 0), tile)

    # Display score
    textScore = font.render(f'Score: {score}', True, (255, 50, 50))
    window.blit(textScore, (35, 35))

    # Display the remaining time
    remaining_time = max(0, (game_duration - elapsed_time) // 1000)
    textTime = font.render(f'Time: {remaining_time}s', True, (255, 50, 50))
    window.blit(textTime, (width - 200, 35))

    # Update the display
    pygame.display.update()
    clock.tick(fps)

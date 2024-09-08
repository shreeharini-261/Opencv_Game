import cv2
import numpy as np
import random

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Define the initial position and size of the player's avatar
avatar_pos = 300
avatar_width = 100
avatar_height = 100

# Define object parameters
object_width = 50
object_height = 50
object_speed = 5

# Initialize objects list
objects = []

# Game variables
score = 0
game_over = False
difficulty = 1

# Function to detect the player's position using color detection
def detect_player(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([0, 120, 70])
    upper_color = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour, assuming it's the player
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2  # Return the horizontal center of the player
    return avatar_pos

# Function to check for collisions between the avatar and objects
def check_collision(avatar_pos, object_pos):
    avatar_rect = (avatar_pos - avatar_width//2, 480 - avatar_height, avatar_width, avatar_height)
    object_rect = (object_pos[0], object_pos[1], object_width, object_height)
    
    if (avatar_rect[0] < object_rect[0] + object_rect[2] and
        avatar_rect[0] + avatar_rect[2] > object_rect[0] and
        avatar_rect[1] < object_rect[1] + object_rect[3] and
        avatar_rect[1] + avatar_rect[3] > object_rect[1]):
        return True
    return False

# Main game loop
while not game_over:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    height, width, _ = frame.shape

    # Detect player position
    avatar_pos = detect_player(frame)
    
    # Draw the player's avatar
    cv2.rectangle(frame, (avatar_pos - avatar_width//2, 480 - avatar_height), 
                  (avatar_pos + avatar_width//2, 480), (0, 255, 0), -1)
    
    # Add new objects
    if random.randint(1, 20) == 1:
        new_object_pos = [random.randint(0, width - object_width), 0]
        objects.append(new_object_pos)
    
    # Move and draw objects
    for object_pos in objects:
        object_pos[1] += object_speed
        cv2.rectangle(frame, (object_pos[0], object_pos[1]), 
                      (object_pos[0] + object_width, object_pos[1] + object_height), 
                      (0, 0, 255), -1)
        
        # Check for collision
        if check_collision(avatar_pos, object_pos):
            game_over = True
    
    # Increase difficulty over time
    difficulty += 0.01
    object_speed = int(difficulty)

    # Remove off-screen objects
    objects = [obj for obj in objects if obj[1] < height]

    # Display score
    score += 1
    cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Display the game frame
    cv2.imshow('Object Dodging Game', frame)
    
    # Break the loop if the player presses 'q' or if the game is over
    if cv2.waitKey(10) & 0xFF == ord('q') or game_over:
        break

# Display Game Over message
cv2.putText(frame, "Game Over", (width // 2 - 100, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
cv2.imshow('Object Dodging Game', frame)
cv2.waitKey(2000)

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

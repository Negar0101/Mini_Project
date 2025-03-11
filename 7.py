import pygame
import random
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

targets = []

def check_target(new_x, new_y):
    for target in targets:
        dist = math.sqrt((new_x - target.x) ** 2 + (new_y - target.y) ** 2)
        if dist < 60:
            return True
    return False

class Target:
    def __init__(self):
        self.R = 30
        self.color = green
        self.position()

    def position(self):
        while True:
            new_x = random.randint(self.R, width - self.R)
            new_y = random.randint(100, height - self.R)
            if not check_target(new_x, new_y):
                self.x = new_x
                self.y = new_y
                break

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.R)

for i in range(3):
    targets.append(Target())

class Player:
    def __init__(self, color, keys, save_key):
        self.x = random.randint(5, width - 5)
        self.y = random.randint(70, height - 5)
        self.color = color
        self.keys = keys
        self.save_key = save_key
        self.dots = []
        self.bullet = 10  
        self.time = 60 

    def move(self, event):
        if event.type == pygame.KEYDOWN and self.bullet > 0:  
            newy = self.y
            newx = self.x
            if event.key == self.keys["left"]:
                newx -= 25
                if newx >= 5:
                    self.x -= 50
                      
            if event.key == self.keys["right"]:
                newx += 25
                if newx <= width - 5:
                    self.x += 25
                     
            if event.key == self.keys["up"]:
                newy -= 25
                if newy >= 80:
                    self.y -= 25
                     
            if event.key == self.keys["down"]:
                newy += 25
                if newy <= height - 5:
                    self.y += 25
                      

    def positions(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.save_key:
            self.dots.append((self.x, self.y))
            self.bullet-=1

            
    def draw_dots(self):
        for dot in self.dots:
            pygame.draw.circle(screen, self.color, dot, 5)

player1 = Player(red, {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}, pygame.K_TAB)
player2 = Player(blue, {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}, pygame.K_RETURN)

font = pygame.font.SysFont("Comic Sans MS", 15)
left_texts = ["Player 1 Score : 0", f"Bullet : {player1.bullet}"]
right_texts = ["Player 2 Score : 0", f"Bullet : {player2.bullet}"]
colors = [red, blue]

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(white)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player1.positions(event)
        player2.positions(event)
        player1.move(event)
        player2.move(event)

    
    player1.time = max(0, player1.time - 1 / 60)
    player2.time = max(0, player2.time - 1 / 60)

    
    if player1.time == 0 or player2.time == 0:
        running = False  
    if player1.bullet == 0 or player2.bullet == 0:
        running = False
    player1_time_display = font.render(f"Time: {int(player1.time)}", True, black)
    player2_time_display = font.render(f"Time: {int(player2.time)}", True, black)
    screen.blit(player1_time_display, (20, 10))
    screen.blit(player2_time_display, (width - 180, 10))

    
    left_texts[1] = f"Bullet : {player1.bullet}"
    right_texts[1] = f"Bullet : {player2.bullet}"

   
    start_y = 30
    for i in range(len(left_texts)):
        left_rendered = font.render(left_texts[i], True, red)
        screen.blit(left_rendered, (20, start_y))
        right_rendered = font.render(right_texts[i], True, blue)
        screen.blit(right_rendered, (width - 180, start_y))
        start_y += left_rendered.get_height()

    
    for target in targets:
        target.display(screen)
    
    player1.draw_dots()
    player2.draw_dots()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

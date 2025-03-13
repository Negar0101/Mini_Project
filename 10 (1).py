import pygame
import random
import math

pygame.init()

width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

targets = []
bars = []
special_items = []

class GameObject:
    def __init__(self, color, x=None, y=None):
        self.x = x or random.randint(0, width)
        self.y = y or random.randint(100, height)
        self.color = color
    
    def check_circle(self, R, list_of_bars):
        self.R = R
        for b in list_of_bars:
            for x in range(self.x - self.R, self.x + self.R):
                for y in range(self.y - self.R, self.y + self.R):
                    if (b.x <= x <= b.x + b.width) and (b.y <= y <= b.y + b.height):
                        return True
            if (self.x - self.R <= b.x + b.width and self.x + self.R >= b.x and
                self.y - self.R <= b.y + b.height and self.y + self.R >= b.y):
                return True
        return False
    
    def check_bar(self, width, height, list_of_targets):
        self.width = width
        self.height = height
        for t in list_of_targets:
            for x in range(self.x, self.x + self.width):
                for y in range(self.y, self.y + self.height):
                    if t.x - t.R <= x <= t.x + t.R and t.y - t.R <= y <= t.y + t.R:
                        return True
        return False
    
    def display_circle(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.R)
    
    def display_bar(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

class Target(GameObject):
    def __init__(self):
        super().__init__(color=green)
        self.R = 30
        self.position()

    def check_target(self, new_x, new_y, targets):
        for target in targets:
            dist = math.sqrt((new_x - target.x) ** 2 + (new_y - target.y) ** 2)
            if dist < 60:
                return True
        return False

    def position(self):
        while True:
            self.x = random.randint(self.R, width - self.R)
            self.y = random.randint(100, height - self.R)
            if self.check_target(self.x, self.y, targets):
                continue
            if self.check_circle(self.R, bars):
                continue

            
            if self.check_target(self.x, self.y, special_items):
                continue
            break
    
    def display(self, screen):
        self.display_circle(screen)

for i in range(3):
    targets.append(Target())

class Player(GameObject):
    def __init__(self, color, keys, save_key):
        super().__init__(x=random.randint(5, width - 5), y=random.randint(100, height - 5), color=color)
        self.keys = keys
        self.save_key = save_key
        self.dots = []
        self.bullet = 10
        self.time = 60
        self.R = 10
    
    def move(self, event):
        if event.type == pygame.KEYDOWN:
            newx = self.x
            newy = self.y
            if event.key == self.keys["left"]:
                newx -= 25
                if newx >= 5:
                    self.x -= 25
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

    def check_overlap(self):
        return self.check_circle(30, bars)
    
    def display(self, screen):
        
        for dot in self.dots:
            pygame.draw.circle(screen, self.color, (dot[0], dot[1]), self.R)
        
class SpecialItem(Target):
    def __init__(self, item_type):
        super().__init__()
        self.item_type = item_type
        self.lifetime = 1200  
        self.R = 30
        if item_type == "more_bullets":
            self.color = YELLOW
            self.effect = lambda player, opponent: setattr(player, 'bullet', player.bullet + 5)
        elif item_type == "more_time":
            self.color = CYAN
            self.effect = lambda player, opponent: setattr(player, 'time', player.time + 10)
        elif item_type == "quick_score":
            self.color = ORANGE
            self.effect = lambda player, opponent: setattr(player, 'score', player.score + 3)
        elif item_type == "reduce_opponent_bullets":
            self.color = red
            self.effect = lambda player, opponent: setattr(opponent, 'bullet', max(0, opponent.bullet - 3))
        self.position()

    def position(self):
        while True:
            self.x = random.randint(self.R, width - self.R)
            self.y = random.randint(100, height - self.R)
            if self.check_target(self.x, self.y, targets):
                continue
            if self.check_circle(self.R, bars):
                continue
            if self.check_target(self.x, self.y, special_items):
                continue
            break

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0 and self in special_items:
            special_items.remove(self)

    def display(self, screen):
        self.display_circle(screen)
        indicator = small_font.render(self.item_type[0].upper(), True, black)
        time_left = small_font.render(str(self.lifetime // 60), True, black)
        screen.blit(indicator, (self.x - 5, self.y - 5))
        screen.blit(time_left, (self.x + 5, self.y + 5))

class Score(Player):
    def __init__(self, color, keys, save_key):
        super().__init__(color, keys, save_key)
        self.nx = self.x
        self.ny = self.y
        self.score = 0

    def update_position(self):
        self.nx = self.x
        self.ny = self.y

    def shoot(self, targets, bars, special_items):
        if self.bullet > 0 and self.time > 0:
            self.dots.append([self.x, self.y, 0])
            self.bullet -= 1
            print(f"Shot fired! Bullets left: {self.bullet}")

            
            for bar in bars:
                if bar.check_hit(self.x, self.y):
                    self.score -= 1
                    print("Hit a bar! -1 score")
                    return

            
            for target in targets[:]:
                d = math.sqrt((target.x - self.x) ** 2 + (target.y - self.y) ** 2)
                if d <= 40:
                    self.dots[-1][2] = 1  
                    targets.remove(target)
                    new_target = Target()
                    targets.append(new_target)
                    
                    if len(self.dots) > 1:
                        last_dot = self.dots[-2]
                        dist = math.sqrt((self.x - last_dot[0]) ** 2 + (self.y - last_dot[1]) ** 2)
                        if 0 < dist <= 200:
                            self.score += 1
                            print("Distance < 200: +1 score")
                        elif 200 < dist <= 400:
                            self.score += 2
                            print("Distance < 400: +2 score")
                        elif 400 < dist <= 600:
                            self.score += 3
                            print("Distance < 600: +3 score")
                        elif 600 < dist <= 800:
                            self.score += 4
                            print("Distance < 800: +4 score")
                        elif 800 < dist <= 1000:
                            self.score += 5
                            print("Distance < 1000: +5 score")
                        if last_dot[2] == 1:  
                            self.score += 2
                            print("Bonus +2 for consecutive hits!")
                    else:
                        self.score += 1 
                        print("First hit! +1 score")
                    return

            
            for item in special_items[:]:
                d = math.sqrt((item.x - self.x) ** 2 + (item.y - self.y) ** 2)
                if d <= 40:
                    opponent = player1 if self is player2 else player2
                    item.effect(self, opponent)
                    special_items.remove(item)
                    print(f"Collected {item.item_type}!")
                    return

class Bar(GameObject):
    def __init__(self):
        super().__init__(color=black)
        self.width = 70
        self.height = 20
        self.position()

    def position(self):
        while True:
            self.x = random.randint(0, width - self.width)
            self.y = random.randint(70, height - self.height)
            if not self.check_bar(self.width, self.height, targets):
                break

    def check_hit(self, shot_x, shot_y):
        for x in range(shot_x - 5, shot_x + 6):
            for y in range(shot_y - 5, shot_y + 6):
                if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
                    return True
        return False
   
    def display(self, screen):
        self.display_bar(screen)

for j in range(7):
    bars.append(Bar())

player1 = Score(red, {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}, pygame.K_TAB)
player2 = Score(blue, {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}, pygame.K_RETURN)

font = pygame.font.SysFont("Comic Sans MS", 15)
small_font = pygame.font.SysFont("Comic Sans MS", 12)
clock = pygame.time.Clock()

special_types = ["more_bullets", "more_time", "quick_score", "reduce_opponent_bullets"]


spawn_delays = [random.randint(60, 300) for _ in range(3)] 
spawn_counters = [0] * 3

running = True
while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == player1.save_key:
            player1.shoot(targets, bars, special_items)
        if event.type == pygame.KEYDOWN and event.key == player2.save_key:
            player2.shoot(targets, bars, special_items)

        player1.move(event)
        player2.move(event)

    player1.time = max(0, player1.time - 1/60)
    player2.time = max(0, player2.time - 1/60)

    if (player1.time == 0 and player2.time == 0) or (player1.bullet==0 and player2.bullet==0):
        running = False

    
    if len(special_items) < 3:
        for i in range(3 - len(special_items)):
            spawn_counters[i] += 1
            if spawn_counters[i] >= spawn_delays[i]:
                new_item = SpecialItem(random.choice(special_types))
                special_items.append(new_item)
                spawn_delays[i] = random.randint(60, 300)  
                spawn_counters[i] = 0

    
    for item in special_items[:]:
        item.update()

    player1_time_display = font.render(f"Time: {int(player1.time)}", True, black)
    player2_time_display = font.render(f"Time: {int(player2.time)}", True, black)
    screen.blit(player1_time_display, (20, 10))
    screen.blit(player2_time_display, (width - 180, 10))

    left_texts = [f"Player 1 Score: {player1.score}", f"Bullet: {player1.bullet}"]
    right_texts = [f"Player 2 Score: {player2.score}", f"Bullet: {player2.bullet}"]
    start_y = 30
    for i in range(len(left_texts)):
        left_rendered = font.render(left_texts[i], True, red)
        screen.blit(left_rendered, (20, start_y))
        right_rendered = font.render(right_texts[i], True, blue)
        screen.blit(right_rendered, (width - 180, start_y))
        start_y += left_rendered.get_height()

    for target in targets:
        target.display(screen)
    for bar in bars:
        bar.display(screen)
    for item in special_items:
        item.display(screen)
    player1.display(screen)
    player2.display(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
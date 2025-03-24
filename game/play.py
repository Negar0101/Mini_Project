import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UITextEntryLine, UIImage
import random
import math
import os  
os.environ['SDL_VIDEO_CENTERED'] = '1'  # تنظیم محیط برای مرکز کردن پنجره بازی

# راه‌اندازی ماژول Pygame
pygame.init()

# تعریف ابعاد پنجره بازی
WIDTH, HEIGHT = 600, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))  # ایجاد پنجره با ابعاد مشخص
pygame.display.set_caption("Shooting Game")  # تنظیم عنوان پنجره

# تعریف رنگ‌ها به صورت ثابت (RGB)
BLACK = (0, 0, 0)  # سیاه
WHITE = (255, 255, 255)  # سفید
PURPLE = (128, 0, 128)  # بنفش
DARK_PURPLE = (50, 0, 50)  # بنفش تیره
RED = (255, 0, 0)  # قرمز
GREEN = (0, 255, 0)  # سبز
PINK = (255, 105, 180)  # صورتی
BLUE = (0, 0, 255)  # آبی
YELLOW = (255, 255, 0)  # زرد
CYAN = (0, 255, 255)  # فیروزه‌ای
ORANGE = (255, 165, 0)  # نارنجی
GRAY = (150, 150, 150)  # خاکستری
DARK_GRAY = (50, 50, 50)  # خاکستری تیره
LIGHT_RED = (255, 100, 100)  # قرمز روشن
LIGHT_BLUE = (100, 100, 255)  # آبی روشن

# تعریف ثابت‌ها برای صحنه‌های مختلف بازی
MENU_SCENE = 0  # صحنه منوی اصلی
SIGNUP_SCENE = 1  # صحنه ثبت‌نام
LOGIN_SCENE = 2  # صحنه ورود
GAME_SCENE = 3  # صحنه بازی
current_scene = MENU_SCENE  # متغیر برای پیگیری صحنه فعلی (شروع از منو)

# این شئ برای مدیریت صفحه‌ها ایجاد شده
menu_manager = pygame_gui.UIManager((WIDTH, HEIGHT))  # مدیر رابط کاربری برای منوی اصلی
signup_manager = pygame_gui.UIManager((WIDTH, HEIGHT))  # مدیر رابط کاربری برای صفحه ثبت‌نام
login_manager = pygame_gui.UIManager((WIDTH, HEIGHT))  # مدیر رابط کاربری برای صفحه ورود

# ایجاد صفحه پس‌زمینه
background = pygame.Surface((WIDTH, HEIGHT))  # سطحی برای پس‌زمینه با ابعاد پنجره
background.fill(BLACK)  # پر کردن پس‌زمینه با رنگ سیاه

# آپلود و تنظیم آیکون‌ها برای منوی اصلی
icon_shooting_image = pygame.image.load("gun.png").convert_alpha()  # آپلود کردن تصویر اسلحه
icon_shooting_image = pygame.transform.scale(icon_shooting_image, (120, 120))  # تغییر اندازه تصویر اسلحه
icon_target_image = pygame.image.load("target.png").convert_alpha()  # آپلود کردن تصویر هدف
icon_target_image = pygame.transform.scale(icon_target_image, (30, 30))  # تغییر اندازه تصویر هدف

# ایجاد متن عنوان برای منوی اصلی
font = pygame.font.Font(None, 48)  # فونت با اندازه ۴۸ (پیش‌فرض سیستم)
header_surface = font.render("Shooting Game", True, WHITE)  # رندر متن عنوان با رنگ سفید
header_rect = header_surface.get_rect(center=(350, 70))  # تنظیم موقعیت متن در مرکز بالا

# ایجاد دکمه‌ها برای منوی اصلی
start_button = UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 75, 150), (150, 50)), text="Sign Up", manager=menu_manager, tool_tip_text="Create a new account")  # دکمه ثبت‌نام در مختصات ((600/2 - 75), 150) با اندازه (150, 50)
login_button = UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 75, 250), (150, 50)), text="Log In", manager=menu_manager, tool_tip_text="Access existing account")  # دکمه ورود در مختصات مرکزی
exit_button = UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 75, 350), (150, 50)), text="Exit", manager=menu_manager, tool_tip_text="Quit the game")  # دکمه خروج در مختصات مرکزی

icon_positions = [(190, 260), (190, 360), (380, 160), (380, 260), (380, 360), (190, 160)]  # لیستی از مختصات برای قرار دادن آیکون‌های هدف در منو

# صفحه ثبت‌نام (Sign Up)
signup_font = pygame.font.Font(None, 28)  # فونت با اندازه ۲۸ برای صفحه ثبت‌نام
signup_header_surface = signup_font.render("Shooting Game", True, WHITE)  # متن عنوان صفحه ثبت‌نام
signup_header_image = pygame.image.load("gun.png").convert_alpha()  # تصویر اسلحه برای عنوان
signup_header_image = pygame.transform.scale(signup_header_image, (80, 80))  # تغییر اندازه تصویر اسلحه

# آیکون‌های تزئینی و کاربردی صفحه ثبت‌نام
icon_new_image_signup = pygame.image.load("target.png").convert_alpha()  # تصویر هدف برای تزئین
icon_new_image_signup = pygame.transform.scale(icon_new_image_signup, (100, 100))  # تغییر اندازه تصویر هدف
icon_username_image_signup = pygame.image.load("user (3).png").convert_alpha()  # تصویر آیکون کاربر
icon_username_image_signup = pygame.transform.scale(icon_username_image_signup, (25, 25))  # تغییر اندازه آیکون کاربر
icon_password_image_signup = pygame.image.load("padlock (3).png").convert_alpha()  # تصویر آیکون قفل
icon_password_image_signup = pygame.transform.scale(icon_password_image_signup, (25, 25))  # تغییر اندازه آیکون قفل

icon_new_positions_signup = [(40, 100), (100, 450), (300, 0), (250, 400), (560, 250), (480, 200), (80, 300), (500, 350), (400, 300), (500, 50), (130, 210)]  # مختصات آیکون‌های هدف در صفحه ثبت‌نام

# قسمت نام کاربری در صفحه ثبت‌نام
username_label_signup = UILabel(relative_rect=pygame.Rect((200, 170), (100, 30)), text="Username:", manager=signup_manager)  # برچسب "Username:" در مختصات (200, 170) با اندازه (100, 30)
input_box_username_signup = UITextEntryLine(relative_rect=pygame.Rect((210, 200), (175, 30)), manager=signup_manager)  # فیلد متنی برای ورود نام کاربری
icon_username_signup = UIImage(relative_rect=pygame.Rect((180, 202), (25, 25)), image_surface=icon_username_image_signup, manager=signup_manager)  # تصویر کاربر در کنار جعبه متن

# قسمت رمز عبور در صفحه ثبت‌نام
password_label_signup = UILabel(relative_rect=pygame.Rect((200, 240), (100, 30)), text="Password:", manager=signup_manager)  # برچسب "Password:"
input_box_password_signup = UITextEntryLine(relative_rect=pygame.Rect((210, 270), (175, 30)), manager=signup_manager)  # فیلد متنی برای ورود رمز عبور
icon_password_signup = UIImage(relative_rect=pygame.Rect((180, 272), (25, 25)), image_surface=icon_password_image_signup, manager=signup_manager)  # تصویر قفل در کنار جعبه متن

# دکمه پایانی صفحه ثبت‌نام
signup_login_button = UIButton(relative_rect=pygame.Rect((200, 350), (200, 40)), text='Sign Up', manager=signup_manager)  # دکمه "Sign Up" برای ثبت‌نام

# حلقه‌ای که آیکون‌های هدف را در مختصات مشخص‌شده قرار می‌دهد
icon_new_images_signup = []  # لیست برای ذخیره آیکون‌های هدف
for pos in icon_new_positions_signup:
    icon = UIImage(relative_rect=pygame.Rect(pos, (30, 30)), image_surface=icon_new_image_signup, manager=signup_manager)  # ایجاد آیکون هدف در هر موقعیت
    icon_new_images_signup.append(icon)  # اضافه کردن آیکون به لیست

# ایجاد صفحه ورود (Login)
login_font = pygame.font.Font(None, 28)  # فونت با اندازه ۲۸ برای صفحه ورود
login_header_surface = login_font.render("Shooting Game", True, (255, 255, 255))  # متن عنوان صفحه ورود

login_header_image = pygame.image.load("gun.png").convert_alpha()  # تصویر اسلحه برای عنوان
login_header_image = pygame.transform.scale(login_header_image, (80, 80))  # تغییر اندازه تصویر اسلحه

# آیکون‌های صفحه ورود
icon_username_image_login = pygame.image.load("user (3).png").convert_alpha()  # تصویر آیکون کاربر
icon_username_image_login = pygame.transform.scale(icon_username_image_login, (25, 25))  # تغییر اندازه آیکون کاربر
icon_password_image_login = pygame.image.load("padlock (3).png").convert_alpha()  # تصویر آیکون قفل
icon_password_image_login = pygame.transform.scale(icon_password_image_login, (25, 25))  # تغییر اندازه آیکون قفل
icon_new_image_login = pygame.image.load("target.png").convert_alpha()  # تصویر هدف برای تزئین
icon_new_image_login = pygame.transform.scale(icon_new_image_login, (100, 100))  # تغییر اندازه تصویر هدف

icon_new_positions_login = [(40, 100), (100, 450), (300, 0), (250, 400), (560, 250), (480, 200), (80, 300), (500, 350), (400, 300), (500, 50), (130, 210)]  # مختصات آیکون‌های هدف در صفحه ورود
icon_new_images_login = []  # لیست برای ذخیره آیکون‌های هدف
for pos in icon_new_positions_login:
    icon = UIImage(relative_rect=pygame.Rect(pos, (30, 30)), image_surface=icon_new_image_login, manager=login_manager)  # ایجاد آیکون هدف در هر موقعیت
    icon_new_images_login.append(icon)  # اضافه کردن آیکون به لیست

# قسمت نام کاربری در صفحه ورود
username_label_login = UILabel(relative_rect=pygame.Rect((200, 170), (100, 30)), text="Username:", manager=login_manager)  # برچسب "Username:"
input_box_username_login = UITextEntryLine(relative_rect=pygame.Rect((210, 200), (175, 30)), manager=login_manager)  # فیلد متنی برای ورود نام کاربری
icon_username_login = UIImage(relative_rect=pygame.Rect((180, 202), (25, 25)), image_surface=icon_username_image_login, manager=login_manager)  # تصویر کاربر در کنار جعبه متن

# قسمت رمز عبور در صفحه ورود
password_label_login = UILabel(relative_rect=pygame.Rect((200, 240), (100, 30)), text="Password:", manager=login_manager)  # برچسب "Password:"
input_box_password_login = UITextEntryLine(relative_rect=pygame.Rect((210, 270), (175, 30)), manager=login_manager)  # فیلد متنی برای ورود رمز عبور
icon_password_login = UIImage(relative_rect=pygame.Rect((180, 272), (25, 25)), image_surface=icon_password_image_login, manager=login_manager)  # تصویر قفل در کنار جعبه متن

# دکمه پایانی صفحه ورود
login_signup_button = UIButton(relative_rect=pygame.Rect((200, 350), (200, 40)), text='Log In', manager=login_manager)  # دکمه "Log In" برای ورود

class GameObject:
    def __init__(self, color, x=None, y=None):
        self.x = x or random.randint(0, 800)
        self.y = y or random.randint(100, 700)
        self.color = color
    # بررسی برخورد دایره با میله
    def check_clash_of_circle_with_bar(self, R, list_of_bars): 
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
    # بررسی برخورد میله با دایره
    def check_clash_of_bar_with_circle(self, width, height, list_of_targets):
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
        super().__init__(color=GREEN)
        self.R = 30
        self.position()
    # بررسی این که هدف های قبلی با هدف جدید برخورد دارند یا خیر
    def check_target(self, new_x, new_y, targets):
        for target in targets:
            if target is not self:    
                dist = math.sqrt((new_x - target.x) ** 2 + (new_y - target.y) ** 2)
                if dist < 2*self.R:
                    return True
        return False
    # تعیین موقعیت جدید برای هدف
    def position(self):
        while True:
            self.x = random.randint(self.R, 800 - self.R)
            self.y = random.randint(100+10, 700 - self.R)
            if self.check_target(self.x, self.y, targets):
                continue
            if self.check_clash_of_circle_with_bar(self.R, bars):
                continue
            if self.check_target(self.x, self.y, special_items):
                continue
            break
    
    def display(self, screen):
        self.display_circle(screen)

class Player(GameObject):
    def __init__(self, color, keys, save_key):
        super().__init__(x=random.randint(5, 800 - 10), y=random.randint(100+10, 700 - 10), color=color)
        self.keys = keys
        self.save_key = save_key
        self.dots = []
        self.bullet = 10
        self.time = 60
        self.R = 10
    #حرکت بازیکن ها
    def move(self, event):
        if event.type == pygame.KEYDOWN:
            newx, newy = self.x, self.y
            if event.key == self.keys["left"]:
                newx -= 25
                if newx >= 10:
                    self.x -= 25
            if event.key == self.keys["right"]:
                newx += 25
                if newx <= 800 - 10:
                    self.x += 25
            if event.key == self.keys["up"]:
                newy -= 25
                if newy >= 100 + 10:
                    self.y -= 25
            if event.key == self.keys["down"]:
                newy += 25
                if newy <= 700 - 10:
                    self.y += 25
    
    #شلیک ها را در صفحه می کشد   
    def display_dots(self, screen):
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
            self.effect = lambda player ,opponent: setattr(player, 'bullet', player.bullet + 5)
        elif item_type == "more_time":
            self.color = CYAN
            self.effect = lambda player ,opponent: setattr(player, 'time', player.time + 10)
        elif item_type == "quick_score":
            self.color = ORANGE
            self.effect = lambda player , opponent: setattr(player, 'score', player.score + 3)
        elif item_type == "reduce_opponent_bullets":
            self.color = PINK
            self.effect = lambda player, opponent: setattr(opponent, 'bullet', max(0, opponent.bullet - 3))
        self.position()

    def position(self):
        while True:
            self.x = random.randint(self.R, 800 - self.R)
            self.y = random.randint(100+self.R, 700 - self.R)
            if self.check_target(self.x, self.y, targets):
                continue
            if self.check_clash_of_circle_with_bar(self.R, bars):
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
        indicator = small_font.render(self.item_type[0].upper(), True, BLACK)
        screen.blit(indicator, (self.x, self.y))
        
# امتیاز محاسبه می کند
class Score(Player):
    def __init__(self, color, keys, save_key):
        super().__init__(color, keys, save_key)
        self.score = 0

    def shoot(self, targets, bars, special_items):
        if self.bullet > 0 and self.time > 0: #بررسی اینکه مجاز به تیر اندازی است  
            self.dots.append([self.x, self.y, 0])#اضافه کردن  شلیک به لیست برای رسم
            self.bullet -= 1
            shoot_sound.play()
            #بررسی برخورد  شلیک با میله
            for bar in bars:
                if bar.check_hit_of_shot(self.x, self.y):
                    self.score -= 1
                    error_sound.play()
                    return # اگر برخورد شد ادامه نده
            #بررسی برخورد شلیک با هدف
            for target in targets[:]:
                d = math.sqrt((target.x - self.x) ** 2 + (target.y - self.y) ** 2)
                if d <= 40:#R+r=10+30
                    self.dots[-1][2] = 1
                    targets.remove(target)
                    targets.append(Target())
                    if len(self.dots) > 1: #بررسی اینکه قبلا تیراندازی شده یا نه
                        # فاصله آخرین تیر شلیک شده و امتیاز دهی
                        last_dot = self.dots[-2]
                        dist = math.sqrt((self.x - last_dot[0]) ** 2 + (self.y - last_dot[1]) ** 2)
                        if 0 < dist <= 200:
                            self.score += 1
                            score_sound.play()
                        elif 200 < dist <= 400:
                            self.score += 2
                            score_sound.play()
                        elif 400 < dist <= 600:
                            self.score += 3
                            score_sound.play()
                        elif 600 < dist <= 800:
                            self.score += 4
                            score_sound.play()
                        elif 800 < dist <= 1000:
                            self.score += 5
                            score_sound.play()
                        if last_dot[2] == 1:
                            self.score += 2
                    else:# اگر تیر اولین بود
                        self.score += 1
                        score_sound.play()
                    return # اگر برخورد شد ادامه نده
            #بررسی برخورد شلیک با آیتم های مخصوص 
            for item in special_items[:]:
                d = math.sqrt((item.x - self.x) ** 2 + (item.y - self.y) ** 2)
                if d <= 40:
                    opponent = player1 if self is player2 else player2
                    item.effect(self, opponent)
                    specialItem_sound.play()
                    special_items.remove(item)
                    return # اگر برخورد شد ادامه نده

class Bar(GameObject):
    def __init__(self):
        super().__init__(color=BLACK)
        self.width = 70
        self.height = 20
        self.position()

    def position(self):
        while True:
            self.x = random.randint(0, 800 - self.width)
            self.y = random.randint(100, 700 - self.height)
            if not self.check_clash_of_bar_with_circle(self.width, self.height, targets)and  not self.check_two_bar(self.width, self.height, bars):
                break
    #بررسی برخورد شلیک با میله             
    def check_hit_of_shot(self, shot_x, shot_y):
        for x in range(shot_x - 10, shot_x + 10):
            for y in range(shot_y - 10, shot_y +10):
                if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
                    return True
        return False
    #بررسی برخورد دو میله با هم
    def check_two_bar(self, width, height, list_of_bars):
        self.width = width
        self.height = height
        for b in list_of_bars:
            for x in range(self.x, self.x + self.width):
                for y in range(self.y, self.y + self.height):
                    if b.x - b.width <= x <= b.x + b.width and b.y - b.height <= y <= b.y + b.height:
                        return True
        return False
    def display(self, screen):
        self.display_bar(screen)
#تعریف متغیرهای جهانی بازی
targets = []
bars = []
special_items = []
player1 = None
player2 = None
font = None
small_font = None
title_font = None
result_font = None
button_font = None
clock = None
special_types = None
spawn_delays = None
spawn_counters = None

#مقداردهی اولیه بازی
def initialize_game():
    global window, targets, bars, special_items, player1, player2, font, small_font, clock, special_types, spawn_delays, spawn_counters, title_font, result_font, button_font ,shoot_sound,score_sound,specialItem_sound,error_sound
    window = pygame.display.set_mode((800, 700)) 
    targets = []
    for _ in range(3):
        new_target = Target()
        targets.append(new_target)
    bars = []
    for _ in range(7):
        new_bar = Bar()
        bars.append(new_bar)
    special_items = []
    player1 = Score(RED, {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}, pygame.K_TAB)
    player2 = Score(BLUE, {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}, pygame.K_RETURN)
    font = pygame.font.SysFont("Comic Sans MS", 15)
    small_font = pygame.font.SysFont("Comic Sans MS", 12)
    title_font = pygame.font.SysFont("Comic Sans MS", 50, bold=True)
    result_font = pygame.font.SysFont("Comic Sans MS", 30)
    button_font = pygame.font.SysFont("Comic Sans MS", 25)
    clock = pygame.time.Clock()
    special_types = ["more_bullets", "more_time", "quick_score", "reduce_opponent_bullets"]
    spawn_delays = [random.randint(60, 300) for _ in range(3)]
    spawn_counters = [0] * 3
    shoot_sound = pygame.mixer.Sound("shoot.wav")  
    score_sound=pygame.mixer.Sound("score.wav")
    specialItem_sound=pygame.mixer.Sound("SpecialItem.mp3")
    error_sound=pygame.mixer.Sound("error.wav")


def draw_gradient(surface, color1, color2):
    for y in range(700): 
        r = int(color1[0] + (color2[0] - color1[0]) * y / 700)
        g = int(color1[1] + (color2[1] - color1[1]) * y / 700)
        b = int(color1[2] + (color2[2] - color1[2]) * y / 700)
        pygame.draw.line(surface, (r, g, b), (0, y), (800, y))

def draw_button(surface, text, rect, color, hover_color, text_color):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect, 0, 10)
    else:
        pygame.draw.rect(surface, color, rect, 0, 10)
    pygame.draw.rect(surface, BLACK, rect, 3, 10)
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
    return rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

def display_end_screen(winner):
    global running, game_over, current_scene, window  
    animation_timer = 0
    animation_speed = 0.05

    while game_over:
        draw_gradient(window, LIGHT_RED, LIGHT_BLUE)
        
        animation_timer = (animation_timer + animation_speed) % (2 * math.pi)
        title_scale = 1 + 0.1 * math.sin(animation_timer)
        title_text = title_font.render("Game Over!", True, BLACK)
        scaled_title = pygame.transform.scale(title_text, 
                                            (int(title_text.get_width() * title_scale), 
                                             int(title_text.get_height() * title_scale)))
        title_rect = scaled_title.get_rect(center=(800//2, 120))
        window.blit(scaled_title, title_rect)

        box_width, box_height = 500, 350
        box_x, box_y = (800 - box_width) // 2, (700 - box_height) // 2
        shadow_offset = 10
        pygame.draw.rect(window, DARK_GRAY, (box_x + shadow_offset, box_y + shadow_offset, box_width, box_height), 0, 15)
        pygame.draw.rect(window, WHITE, (box_x, box_y, box_width, box_height), 0, 15)
        pygame.draw.rect(window, BLACK, (box_x, box_y, box_width, box_height), 5, 15)

        if winner == "Draw":
            result_text = result_font.render("It's a Draw!", True, GRAY)
        elif winner == "Player 1":
            result_text = result_font.render("Player 1 Wins!", True, RED)
        else:
            result_text = result_font.render("Player 2 Wins!", True, BLUE)
        result_rect = result_text.get_rect(center=(800//2, box_y + 80))
        window.blit(result_text, result_rect)

        score1_text = result_font.render(f"Player 1: {player1.score}", True, RED)
        score2_text = result_font.render(f"Player 2: {player2.score}", True, BLUE)
        score1_rect = score1_text.get_rect(center=(800//2, box_y + 150))
        score2_rect = score2_text.get_rect(center=(800//2, box_y + 200))
        window.blit(score1_text, score1_rect)
        window.blit(score2_text, score2_rect)

        replay_rect = pygame.Rect(800//2 - 150, box_y + 260, 120, 50)
        exit_rect = pygame.Rect(800//2 + 30, box_y + 260, 120, 50)
        
        if draw_button(window, "Replay", replay_rect, GRAY, LIGHT_RED, WHITE):
            player1.score = 0
            player1.bullet = 10
            player1.time = 60
            player1.dots = []
            player2.score = 0
            player2.bullet = 10
            player2.time = 60
            player2.dots = []
            targets.clear()
            for i in range(3):
                new_target=Target()
                targets.append(new_target)
            special_items.clear()
            game_over = False
        
        if draw_button(window, "Exit", exit_rect, GRAY, LIGHT_BLUE, WHITE):
            current_scene = MENU_SCENE
            window = pygame.display.set_mode((WIDTH, HEIGHT))  
            game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False

        pygame.display.flip()
        clock.tick(60)


running = True
game_initialized = False
game_over = False

while running:
    # تنظیم زمان برای به‌روزرسانی فریم‌ها (60 فریم در ثانیه)
    time_delta = clock.tick(60) / 1000.0 if game_initialized else pygame.time.Clock().tick(60) / 1000.0
    
    # حلقه رویدادها برای بررسی ورودی‌های کاربر
    for event in pygame.event.get():
        # اگر کاربر پنجره را ببندد، بسته می‌شود
        if event.type == pygame.QUIT:
            running = False
            
        # اگر کلید Escape زده شود، به منوی اصلی برمی‌گردد یا برنامه بسته می‌شود
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if current_scene in (SIGNUP_SCENE, LOGIN_SCENE):
                current_scene = MENU_SCENE
            elif current_scene == GAME_SCENE:
                current_scene = MENU_SCENE
                window = pygame.display.set_mode((WIDTH, HEIGHT))  
            else:
                running = False
                
        # مدیریت رویدادها در صحنه منوی اصلی
        if current_scene == MENU_SCENE:
            menu_manager.process_events(event)
            
        # مدیریت رویدادها در صحنه ثبت‌نام
        elif current_scene == SIGNUP_SCENE:
            signup_manager.process_events(event)
        # مدیریت رویدادها در صحنه ورود
        elif current_scene == LOGIN_SCENE:
            login_manager.process_events(event)
        # مدیریت حرکت و شلیک بازیکنان در صحنه بازی
        elif current_scene == GAME_SCENE and not game_over:
            player1.move(event)
            player2.move(event)
            # شلیک بازیکن ۱ با کلید مشخص‌شده
            if event.type == pygame.KEYDOWN and event.key == player1.save_key:
                player1.shoot(targets, bars, special_items)
            # شلیک بازیکن ۲ با کلید مشخص‌شده
            if event.type == pygame.KEYDOWN and event.key == player2.save_key:
                player2.shoot(targets, bars, special_items)
        
        # بررسی کلیک روی دکمه‌ها و تغییر صحنه‌ها
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # دکمه ثبت‌نام در منوی اصلی
            if event.ui_element == start_button and current_scene == MENU_SCENE:
                current_scene = SIGNUP_SCENE
            # دکمه ورود در منوی اصلی
            elif event.ui_element == login_button and current_scene == MENU_SCENE:
                current_scene = LOGIN_SCENE
            # دکمه خروج در منوی اصلی
            elif event.ui_element == exit_button and current_scene == MENU_SCENE:
                running = False
            # دکمه ثبت‌نام در صفحه ثبت‌نام
            elif event.ui_element == signup_login_button and current_scene == SIGNUP_SCENE:
                username = input_box_username_signup.get_text().strip()
                password = input_box_password_signup.get_text().strip()
                if username and password:  # اگر نام کاربری و رمز وارد شده باشد
                    current_scene = GAME_SCENE
                    if not game_initialized:  # اگر بازی هنوز راه‌اندازی نشده باشد
                        initialize_game()
                        game_initialized = True
            # دکمه ورود در صفحه ورود
            elif event.ui_element == login_signup_button and current_scene == LOGIN_SCENE:
                username = input_box_username_login.get_text().strip()
                password = input_box_password_login.get_text().strip()
                if username and password:  # اگر نام کاربری و رمز وارد شده باشد
                    current_scene = GAME_SCENE
                    if not game_initialized:  # اگر بازی هنوز راه‌اندازی نشده باشد
                        initialize_game()
                        game_initialized = True

    # ترسیم و به‌روزرسانی صحنه منوی اصلی
    if current_scene == MENU_SCENE:
        menu_manager.update(time_delta)
        window.fill(BLACK)  # پر کردن پس‌زمینه با رنگ سیاه
        window.blit(background, (0, 0))  # ترسیم پس‌زمینه
        pygame.draw.rect(window, DARK_PURPLE, (5, 5, WIDTH - 10, HEIGHT - 10), border_radius=15)  #  ترسیم کادر بزرگ بنفش
        pygame.draw.rect(window, PURPLE, (0, 0, WIDTH, HEIGHT), 5, border_radius=15)  # ترسیم حاشیه بنفش
        window.blit(header_surface, header_rect)  # نمایش عنوان بازی
        window.blit(icon_shooting_image, (100, 20))  # نمایش آیکون اسلحه
        for pos in icon_positions:  # نمایش آیکون‌های هدف در موقعیت‌های مشخص
            window.blit(icon_target_image, pos)
        menu_manager.draw_ui(window)  # ترسیم رابط کاربری منو
            
    # ترسیم و به‌روزرسانی صحنه ثبت‌نام
    elif current_scene == SIGNUP_SCENE:
        signup_manager.update(time_delta)
        window.fill(BLACK)  # پر کردن پس‌زمینه با رنگ سیاه
        window.blit(signup_header_image, (170, 90))  # نمایش آیکون اسلحه در بالا
        window.blit(signup_header_surface, (250, 120))  # نمایش عنوان بازی
        pygame.draw.rect(window, PURPLE, (195, 345, 210, 50), 4)  # ترسیم کادر دور دکمه
        signup_manager.draw_ui(window)  # ترسیم رابط کاربری ثبت‌نام
    
    # ترسیم و به‌روزرسانی صحنه ورود
    elif current_scene == LOGIN_SCENE:
        login_manager.update(time_delta)
        window.fill(BLACK)  # پر کردن پس‌زمینه با رنگ سیاه
        window.blit(login_header_image, (170, 90))  # نمایش آیکون اسلحه در بالا
        window.blit(login_header_surface, (250, 120))  # نمایش عنوان بازی
        pygame.draw.rect(window, PURPLE, (195, 345, 210, 50), 4)  # ترسیم کادر دور دکمه
        login_manager.draw_ui(window)  # ترسیم رابط کاربری ورود
    
    # مدیریت و ترسیم صحنه بازی
    elif current_scene == GAME_SCENE:
        if not game_over:  # اگر بازی تمام نشده باشد
            window.fill(WHITE)  # پر کردن پس‌زمینه با رنگ سفید
            # کاهش زمان بازیکنان
            player1.time = max(0, player1.time - 1/60)
            player2.time = max(0, player2.time - 1/60)
            # بررسی پایان بازی (زمان یا گلوله‌ها صفر شود)
            if (player1.time == 0 and player2.time == 0) or (player1.bullet == 0 and player2.bullet == 0):
                game_over = True
                # تعیین برنده بازی
                if player1.score > player2.score:
                    winner = "Player 1"
                elif player2.score > player1.score:
                    winner = "Player 2"
                else:
                    winner = "Draw"
            
            # تولید آیتم‌های ویژه در صورت کمبود
            if len(special_items) < 3:
                for i in range(3 - len(special_items)):
                    spawn_counters[i] += 1
                    if spawn_counters[i] >= spawn_delays[i]:  # اگر زمان تولید فرا رسیده باشد
                        new_item = SpecialItem(random.choice(special_types))
                        special_items.append(new_item)
                        spawn_delays[i] = random.randint(60, 300)  # تنظیم تاخیر جدید
                        spawn_counters[i] = 0  # ریست شمارنده
            
            # به‌روزرسانی آیتم‌های ویژه
            for item in special_items[:]:
                item.update()

            # نمایش زمان باقیمانده بازیکنان
            player1_time_display = font.render(f"Time: {int(player1.time)}", True, BLACK)
            player2_time_display = font.render(f"Time: {int(player2.time)}", True, BLACK)
            window.blit(player1_time_display, (20, 10))
            window.blit(player2_time_display, (800 - 180, 10))

            # نمایش امتیاز و تعداد گلوله‌های بازیکنان
            left_texts = [f"Player 1 Score: {player1.score}", f"Bullet: {player1.bullet}"]
            right_texts = [f"Player 2 Score: {player2.score}", f"Bullet: {player2.bullet}"]
            start_y = 30
            for i in range(len(left_texts)):
                left_rendered = font.render(left_texts[i], True, RED)
                window.blit(left_rendered, (20, start_y))
                right_rendered = font.render(right_texts[i], True, BLUE)
                window.blit(right_rendered, (800 - 180, start_y))
                start_y += left_rendered.get_height()

            # ترسیم اهداف، میله‌ها و آیتم‌های ویژه
            for target in targets:
                target.display(window)
            for bar in bars:
                bar.display(window)
            for item in special_items:
                item.display(window)
            # ترسیم شلیک‌های بازیکنان
            player1.display_dots(window)
            player2.display_dots(window)
        else:
            # نمایش صفحه پایان بازی
            display_end_screen(winner)
    
    # به‌روزرسانی صفحه نمایش
    pygame.display.flip()

# بستن Pygame و پایان برنامه
pygame.quit()

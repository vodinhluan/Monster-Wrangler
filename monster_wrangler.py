import pygame, random
pygame.init()
WIDTH = 1200
HEIGHT = 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Wrangler")

# set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# define the class
class Game():
    def __init__(self, player, monster_group):
        self.score = 0
        self.round_number = 0 #so vong dau
        self.round_time = 0 #thoi gian vong dau
        self.frame_count = 0
        self.player = player
        self.monster_group = monster_group

        #set sound and music
        self.next_level_sound = pygame.mixer.Sound("monster_wrangler/next_level.wav")

        #set font
        self.font = pygame.font.Font("monster_wrangler/abrushow.ttf", 24)

        #set images
        blue_monster = pygame.image.load("monster_wrangler/blue_monster.png")
        green_monster = pygame.image.load("monster_wrangler/green_monster.png")
        pink_monster = pygame.image.load("monster_wrangler/pink_monster.png")
        orange_monster = pygame.image.load("monster_wrangler/orange_monster.png")

        # danh sach tuong ung voi 4 loai quai vat
        # 0 blue 1 green 3 pink 4 yellow
        self.target_monster_images = [blue_monster, green_monster, pink_monster, orange_monster]
        # tao quai vat muc tieu
        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_image_rect = self.target_monster_image.get_rect()
        self.target_monster_image_rect.centerx = WIDTH // 2
        self.target_monster_image_rect.top = 30

    def update(self):
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0
        self.check_collision()

    def draw(self):
        # set colors
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PINK = (226, 73, 243)
        YELLOW = (243, 157, 20)

        # them mau sac cua quai vat vao danh sach sao cho khop voi mau cua quai vat muc tieu
        colors = [BLUE, GREEN, PINK, YELLOW]

        # set text
        catch_text = self.font.render("Target Monster", True, WHITE)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = WIDTH // 2
        catch_text_rect.top = 5

        score_text = self.font.render("SCORE: "+str(self.score), True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (5, 5)

        lives_text = self.font.render("LIVES: "+str(self.player.lives), True, WHITE)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (5, 35)

        round_text = self.font.render("CURRENT ROUND: "+str(self.round_number), True, WHITE)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (5, 65)

        time_text = self.font.render("ROUND TIME: "+str(self.round_time), True, WHITE)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (WIDTH - 10, 5)

        warp_text = self.font.render("WARPS: "+str(self.player.warps), True, WHITE)
        warp_text_rect = warp_text.get_rect()
        warp_text_rect.topright = (WIDTH - 10, 35)


        #blit the hud
        SCREEN.blit(catch_text, catch_text_rect)        
        SCREEN.blit(score_text, score_text_rect)
        SCREEN.blit(lives_text, lives_text_rect)
        SCREEN.blit(round_text, round_text_rect)
        SCREEN.blit(time_text, time_text_rect)
        SCREEN.blit(warp_text, warp_text_rect)
        SCREEN.blit(self.target_monster_image, self.target_monster_image_rect)

        #ve khung vien
        pygame.draw.rect(SCREEN, colors[self.target_monster_type], (WIDTH//2-32, 30, 64, 64), 2) #ve khung nho
        pygame.draw.rect(SCREEN, colors[self.target_monster_type], (0, 100,WIDTH, HEIGHT-200), 2) #ve khung lon



    def check_collision(self):
        # kiem tra va cham giua nguoi choi voi 1 quai vat cu the
        collided_monster =pygame.sprite.spritecollideany(self.player, self.monster_group)

        if collided_monster:
            # neu tieu diet dung quai vat
            if collided_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number
                # xoa quat vât do
                collided_monster.remove(self.monster_group)
                if (self.monster_group):
                    # neu con nhieu quai vat de tieu diet
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    #ket thuc vong dau
                    self.player.reset()
                    self.start_new_round()
            #neu tieu diet sai quai vat
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                # neu thua
                if self.player.lives == 0:
                    self.pause_game("Final Score: "+str(self.score),"Press 'Enter' to continue")
                    self.reset_game()
                self.player.reset()

    def start_new_round(self):
        # set điểm thưởng dựa trên tốc độ kết thúc trò chơi
        self.score += int(10000*self.round_number/(1 + self.round_time)) 

        #reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        #remove any remaining monster from a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        #add monsters to the monster group
        for i in range(self.round_number):
            self.monster_group.add(Monster(random.randint(0, WIDTH-64), random.randint(100, HEIGHT-164), self.target_monster_images[0], 0))
            self.monster_group.add(Monster(random.randint(0, WIDTH-64), random.randint(100, HEIGHT-164), self.target_monster_images[1], 1))
            self.monster_group.add(Monster(random.randint(0, WIDTH-64), random.randint(100, HEIGHT-164), self.target_monster_images[2], 2))
            self.monster_group.add(Monster(random.randint(0, WIDTH-64), random.randint(100, HEIGHT-164), self.target_monster_images[3], 3))
        
        self.choose_new_target()
        self.next_level_sound.play()
    def choose_new_target(self):
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        
        global running
        # set color
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        main_text = self.font.render(main_text, True, WHITE)
        main_text_rect = main_text.get_rect()
        main_text_rect.center = (WIDTH // 2, HEIGHT // 2)

        sub_text = self.font.render(sub_text, True, WHITE)
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (WIDTH // 2, HEIGHT // 2 + 64)

        #DISPLAY THE PAUSE TEXT
        SCREEN.fill(BLACK)
        SCREEN.blit(main_text, main_text_rect)
        SCREEN.blit(sub_text, sub_text_rect)
        pygame.display.update()

        #PAUSE THE GAME
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
    def reset_game(self):
        self.round_number = 0
        self.round_time = 0
        self.score = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("monster_wrangler/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT
    
        self.lives = 5
        self.warps = 2
        self.velocity = 8
        self.catch_sound = pygame.mixer.Sound("monster_wrangler/catch.wav")
        self.die_sound = pygame.mixer.Sound("monster_wrangler/die.wav")
        self.warp_sound = pygame.mixer.Sound("monster_wrangler/warp.wav")
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT - 100:
            self.rect.y += self.velocity


    def warp(self):
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = HEIGHT

    def reset(self):
            self.rect.centerx = WIDTH//2
            self.rect.bottom = HEIGHT

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # monster type is an int 
        # 0 blue 1 green 2 pink 3 yellow
        self.type = monster_type

        # set random motion
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 5)

    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        # if the object approaches the edge of the screen --> bounce by change direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <= 100 or self.rect.bottom >= HEIGHT - 100:
            self.dy = -1 * self.dy
        


# Create a player group and player object
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

# Create a monster group but not create a monser object (note in notion)
my_monster_group = pygame.sprite.Group()


# Create a game object
my_game = Game(my_player, my_monster_group)
my_game.pause_game("Welcome to My Game", "Press Enter to play")
my_game.start_new_round()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # the player want to warp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()
    # fill the display
    SCREEN.fill((0, 0, 0))
    # update and draw the object 
    my_player_group.update()
    my_player_group.draw(SCREEN)

    my_monster_group.update()
    my_monster_group.draw(SCREEN)

    my_game.update()
    my_game.draw()
    # update and tick the clock
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
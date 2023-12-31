import pygame
from sys import exit
import random

pygame.init()
clock = pygame.time.Clock()

#Window
win_height = 665
win_width = 590
window = pygame.display.set_mode((win_width, win_height))

#Images
bird_images = [pygame.image.load("bird_down.png"),
               pygame.image.load("bird_mid.png"),
               pygame.image.load("bird_up.png")]
skyline_image = pygame.image.load("background.jpg")
ground_image = pygame.image.load("ground.jpg")
top_pipe_image = pygame.image.load("pipe_top.png")
bottom_pipe_image = pygame.image.load("pipe bottom.png")
game_over_image = pygame.image.load("game_over.png")
start_image = pygame.image.load("start.png")

#Game Ver
scroll_speed = 1
bird_start_position = (100, 250)
score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    def update(self, user_input):
        #Animate Bird
        if self.alive:
           self.image_index +=1
        if self.image_index >= 30:
           self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        #Gravity and Flap
        self.vel += 0.5
        if self.vel > 7:
           self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        #User Input
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        #Move Pipe
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

            #Score
            global score
            if self.pipe_type == 'bottom':
                if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                    self.enter = True
                if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                    self.exit = True
                if self.enter and self.exit and not self.passed:
                    self.passed = True
                    score += 1

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        #Move Ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

def quit_game():
    #Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

#Game Main Method
def main():
    global score

    #Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    #Setup Pipes
    pipe_timer = 0
    pipe = pygame.sprite.Group()

    #Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))


    run = True
    while run:
        #Quit
        quit_game()

        #Reset Frame
        window.fill((0, 0, 0))

        #User Input
        user_input = pygame.key.get_pressed()

        #Draw BG
        window.blit(skyline_image, (0, 0))

        #Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))

        #Draw - Pipes, Ground and Bird
        pipe.draw(window)
        ground.draw(window)
        bird.draw(window)

        #Show Score
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))

        #Update - Pipes, Ground and Bird
        if bird.sprite.alive:
          pipe.update()
          ground.update()
          bird.update(user_input)

        #Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipe, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            if collision_ground or collision_pipes:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                                    win_height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_z]:
                    score = 0
                    break

        #Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-240, -160)
            y_bottom = y_top + random.randint(120, 140)  + random.randint(70, 130) + bottom_pipe_image.get_height()
            pipe.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipe.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(240, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()


# Menu
def menu():
    global game_stopped

    while game_stopped:
        quit_game()

        #Draw Menu
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, (0, 520))
        window.blit(bird_images[2], (100, 250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2, win_height // 2 - start_image.get_height() // 2))

        #User Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()


menu()

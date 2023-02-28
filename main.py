# Source: https://www.youtube.com/watch?v=AY9MnQ4x3zk&ab_channel=ClearCode
from re import T
from typing import List
import pygame
from sys import exit
from random import randint, choice
from pygame import Surface

# [X] TODO: upload to github
# [ ] TODO: fix player jumping on start of game
# [ ] TODO: un/pause
# [ ] TODO: un/mute/dynamic music, prevent game from not starting when there is no audio
# [ ] TODO: dynamic window size, fullscreen
# [ ] TODO: health, three hits and dies
# [ ] TODO: change color of player
# [ ] TODO: save scores


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.walk_animations: List[T] = [player_walk_1, player_walk_2]
        self.jump_sprite = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.animation_index: float = 0

        self.image = self.walk_animations[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (80, FLOOR))
        self.gravity : int = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def update(self):
        # applies a jump
        self.input()
        # changes the position
        self.apply_gravity()
        # updates animation based on position and time
        self.animate()

    def input(self):
        space_key : bool = pygame.key.get_pressed()[pygame.K_SPACE]
        left_mouse : bool = pygame.mouse.get_pressed()[0]
        # if the player is on the floor and, the mouse is clicked on the player or
        # the space bar is pressed, the player will jump
        if self.rect.bottom == FLOOR and (space_key or left_mouse):
            self.gravity = -20
            # play jump sound
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += GRAVITY
        self.rect.bottom += self.gravity
        # if the player is under the floor set the player on the floor
        # and reset the gravity to prevent integer overflow
        if self.rect.bottom > FLOOR:
            self.rect.bottom = FLOOR
            self.gravity = 0

    def animate(self, ANIMATION_SPEED : float = 0.1):
        # player is in the air on the floor
        if self.rect.bottom < FLOOR:
            # display the jump surface when the player is not on the floor
            self.image = self.jump_sprite
        else:
            # play walking animation if the player is on the floor
            # reset the player sprite animation index to 0 whenever
            # it's greater than the length of the animation list
            self.animation_index = (self.animation_index + ANIMATION_SPEED) % len(self.walk_animations)
            self.image = self.walk_animations[int(self.animation_index)]

    def reset(self):
        self.gravity = 0
        self.rect.bottom = FLOOR
        self.animation_index = 0
        self.image = self.walk_animations[self.animation_index]


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame_1: Surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2: Surface = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.animation_frames: List[T] = [fly_frame_1, fly_frame_2]
            self.animation_speed = 0.3
            y_position = FLOOR - 90

        elif type == 'snail':
            snail_frame_1: Surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2: Surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.animation_frames: List[T] = [snail_frame_1, snail_frame_2]
            self.animation_speed = 0.1
            y_position = FLOOR

        self.speed : int = 5
        self.animation_index : int = 0
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_position))

    def update(self):
        # move obstacle toward the left of the screen
        self.rect.left -= self.speed
        self.destroy()
        self.animate()

    def animate(self):
        # reset the sprite animation index to 0 whenever
        # it's greater than the length of the animation list
        self.animation_index = (self.animation_index + self.animation_speed) % len(self.animation_frames)
        self.image = self.animation_frames[int(self.animation_index)]

    def destroy(self):
        # delete the obstacle when it completely crosses the left side of the screen
        if self.rect.right < 0:
            self.kill()


def player_collided() -> bool:
    # returns true if player collided with any of the obstacles
    return not pygame.sprite.spritecollide(player.sprite, obstacles, False)


def display_score():
    global score
    score = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (WIDTH / 2, 50))
    screen.blit(score_surf, score_rect)


def display_title_screen():
    # display background color
    screen.fill((94, 129, 162))
    # display player
    screen.blit(player_stand, player_stand_rect)
    # display title
    screen.blit(game_name, game_name_rect)
    if score:
        # display score
        score_message = game_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (WIDTH / 2, 370))
        screen.blit(score_message, score_message_rect)
    else:
        # display text to start the game
        screen.blit(game_message, game_message_rect)


pygame.init()
pygame.mixer.init()
# GLOBAL/STATIC SETTINGS
WIDTH = 800
HEIGHT = 468
TITLE = 'Pixel Runner'
FPS = 60 # frames per second
FLOOR = 300
game_active = False
start_time = 0
score = 0
GRAVITY : int = 1
BG_MUSIC = pygame.mixer.Sound('audio/music.wav') # background music
BG_MUSIC.set_volume(0.07)
BG_MUSIC.play(loops = -1) # loop forever

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
game_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# player surface scaled for the intro scene
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (WIDTH / 2, HEIGHT / 2))

game_name = game_font.render(TITLE, False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (WIDTH / 2, 100))

game_message = game_font.render('PRESS SPACE TO RUN', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (WIDTH / 2, 370))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700) # trigger evey x milliseconds

# Groups

player : pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
player.add(Player())

obstacles : pygame.sprite.Group = pygame.sprite.Group()

while True:

    # check for input
    for event in pygame.event.get():
        # close window on quit
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()
        elif game_active:
            # spawn a fly or snail every so... seconds
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            # restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # BLIT => BLock Image Transfer
        screen.blit(sky_surface,  (0, 0))
        screen.blit(ground_surface, (0, FLOOR))
        display_score()
        # ---------------------- player movement ----------------------
        player.update()
        player.draw(screen)
        # ---------------------- Obstacle movement --------------------
        obstacles.update()
        obstacles.draw(screen)
        # ---------------------- Collisions ---------------------------
        game_active = player_collided()
        # ---------------------- Clean up ---------------------------
        if not game_active:
            obstacles.empty()
            player.sprite.reset()
    else:
        display_title_screen()

    # draw all our elements
    # update everything
    pygame.display.update()

    # run this loop no more than 60 times per second
    # this loop will only run a max of 60 times a second
    clock.tick(FPS)

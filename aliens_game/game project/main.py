import pygame, sys
import os
import random
from pygame import mixer

#audio settings 
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
mixer.init()
pygame.init()

#music and sounds
music = pygame.mixer.Sound('game project/music/Ripleys Rescues.mp3')
gameover_music = pygame.mixer.Sound('game project/music/gameover1.wav')
alien_screem = pygame.mixer.Sound('game project/music/hiss2.wav')
explosion_sound = pygame.mixer.Sound('game project/music/explosion.wav')

#keep track of lives
player_lives = 3 

#keeps track of score
score = 0 

#aliens images                                                   
aliens = ['facehugger1', 'facehugger2', 'chestburster4', 'chestburster3', 'bomb', 'xeno']    

# game display settings
WIDTH = 800
HEIGHT = 500
FPS = 12                                           
pygame.init()
pygame.display.set_caption('ALIENS-Invasion')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   
clock = pygame.time.Clock()


#  colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BROWN = (150,150,150)
 #cursor display
new_cursor = pygame.image.load('game project/images/crosshair1.png')
pygame.mouse.set_visible(False)

#image and text variables
back = pygame.image.load('game project/images/back.gif') 
background = pygame.image.load('game project/images/background.png')                                  
font = pygame.font.Font(os.path.join(os.getcwd(), 'game project/Robot9000Italic-YzxE8.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))    
lives_icon = pygame.image.load('game project/images/white_lives.png')                    

# aliens positions and when to spawn
def generate_random_aliens(alien):
    alien_path = "game project/images/" + alien + ".png"
    data[alien] = {
        'img': pygame.image.load(alien_path),
        'x' : random.randint(200,500),          
        'y' : 800,
        'speed_x': random.randint(-10,10),      
        'speed_y': random.randint(-80, -60),    
        'throw': False,                         
        't': 0,                                 
        'hit': False,
    }

   
    if random.random() >= 0.75:     
        data[alien]['throw'] = True
    else:
        data[alien]['throw'] = False

#  data for random aliens 
data = {}
for alien in aliens:
    generate_random_aliens(alien)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("game project/images/red_lives.png"), (x, y))

# draw fonts on the screen
def draw_text(display, text, size, x, y):
    font = pygame.font.Font('game project/Robot9000Italic-YzxE8.ttf', 60)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)


# draw players lives
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       
        img_rect.x = int(x + 35 * i)    
        img_rect.y = y                  
        display.blit(img, img_rect)

# show game over display & front display
def show_gameover_screen():
    gameDisplay.blit(back, (0,0))
    draw_text(gameDisplay, "ALIENS!", 90, WIDTH / 2, HEIGHT / 4)
    if not game_over :
        draw_text(gameDisplay,"Enemys killed : " + str(score), 50, WIDTH / 2, HEIGHT /2)

    draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                music.play()
# Game Loop
first_round = True
game_over = True        
game_running = True     
while game_running :
    if game_over :
        if first_round :
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, 'game project/images/red_lives.png')
        score = 0
        
    
    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False
       
    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'game project/images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']          
            value['y'] += value['speed_y']          
            value['speed_y'] += (1 * value['t'])   
            value['t'] += 1                         

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    
            else:
                generate_random_aliens(key)

            #mouse settings and image
            current_position = pygame.mouse.get_pos()   
            gameDisplay.blit(new_cursor, current_position)




            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+100 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+100:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:                        
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)
                    if player_lives < 0 :
                        #stops the main music file to hear the game over file
                        music.stop()
                        #plays sound file for the game end
                        gameover_music.play()
                        #changes to game over screen      
                        show_gameover_screen()    
        
                        game_over = True

                    #if game over screens active then cursor appears    
                    if game_over == True:
                        pygame.mouse.set_visible(True)

                
                    #loads images for if destroyed load killed aliens 
                    half_alien_path = "game project/images/explosion.png"
                    explosion_sound.play()
                else:
                    half_alien_path = "game project/images/" + "killed_" + key + ".png"
                    alien_screem.play()
                value['img'] = pygame.image.load(half_alien_path)
                value['speed_x'] += 80
                if key != 'bomb' :
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_random_aliens(key)
    



    pygame.display.update()
    clock.tick(FPS)      
                        

pygame.quit()

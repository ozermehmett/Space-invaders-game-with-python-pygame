import pygame, sys, random

pygame.init()
W, H = 700, 700
BLACK = (0,0,0)
screen = pygame.display.set_mode((W, H))
bullet_fired = False
game_over = False
bullet_speed = 10
fire = pygame.mixer.Sound("sounds/fire.mp3")
death = pygame.mixer.Sound("sounds/death.mp3")
gameOver = pygame.mixer.Sound("sounds/gameOver.mp3")
background = pygame.image.load("pics/background.png")  #resimleri ekledik
image1 = pygame.image.load('pics/pngegg.png')
imageBullet = pygame.image.load('pics/bullet.png')
monster_img = pygame.image.load('pics/monster.png')
background = pygame.transform.scale(background, (W, H))
imageBullet = pygame.transform.scale(imageBullet, (50, 50))
image1 = pygame.transform.scale(image1, (50, 50))
konum = image1.get_rect(center=(300, 300))
konumBullet = imageBullet.get_rect(center=konum.center)
monster_img = pygame.transform.scale(monster_img, (50, 50))
monster_list = []
monster_speed = 1
monster_spawn_delay = 1000   #canavarlarin dogma sıklıgı
last_monster_spawn_time = pygame.time.get_ticks()   #canavarin dogdugu ani bi degiskene atadik
pygame.display.set_caption('My Game')
pygame.display.update()
clock = pygame.time.Clock()

def gameover():
    gameOver.play()
    font = pygame.font.SysFont('Comic Sans MS', 48)
    gameover_text = font.render("GAME OVER", True, (255, 255, 255))
    gameover_rect = gameover_text.get_rect(center=(W/2, H/2))
    screen.blit(gameover_text, gameover_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    tuslar = pygame.key.get_pressed()
    
    if tuslar[pygame.K_LEFT]:
        konum.move_ip(-10, 0)
    elif tuslar[pygame.K_RIGHT]:
        konum.move_ip(10, 0)
    elif tuslar[pygame.K_UP]:
        konum.move_ip(0, -10)
    elif tuslar[pygame.K_DOWN]:
        konum.move_ip(0, 10)
    if tuslar[pygame.K_SPACE] and not bullet_fired:
        konumBullet.center = konum.center
        fire.play()
        bullet_fired = True
        
    if konum.left < 0:
        konum.left = 0
    elif konum.right > W:
        konum.right = W
    if konum.top < 0:
        konum.top = 0
    elif konum.bottom > H:
        konum.bottom = H

    if pygame.time.get_ticks() - last_monster_spawn_time > monster_spawn_delay:
        last_monster_spawn_time = pygame.time.get_ticks()
        monster_x = random.randint(0, W - monster_img.get_width())
        monster_rect = monster_img.get_rect(midtop=(monster_x, 0))
        monster_list.append(monster_rect)

    for monster_rect in monster_list:
        monster_rect.move_ip(0, monster_speed)
        if monster_rect.top > H:
            monster_list.remove(monster_rect)
        elif monster_rect.colliderect(konum):
            gameover()
            monster_list.clear()
            bullet_fired = False
            konum.center = (W/2, H/2)
            game_over = True

    if bullet_fired:
        konumBullet.move_ip(0, -bullet_speed)
        if konumBullet.bottom < 0:
            bullet_fired = False

    screen.blit(background, (0, 0))
    screen.blit(image1,konum)
    for monster_rect in monster_list:
        screen.blit(monster_img, monster_rect)

    for monster_rect in monster_list:
        if konumBullet.colliderect(monster_rect):
            monster_list.remove(monster_rect)
            bullet_fired = False
            death.play()
            break

    if bullet_fired:
        screen.blit(imageBullet, konumBullet)
    
    if game_over:
        monster_list.clear()
        bullet_fired = False
        konum.center = (W/2, H/2)
        game_over = False
        continue
    
    pygame.display.update()
    clock.tick(60)
    
    

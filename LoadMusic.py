import pygame

pygame.init()
pygame.mixer.init()

# music for background music
pygame.mixer.music.load("./music/bgm.wav")
pygame.mixer.music.set_volume(5)

# music for heroplane shooting bullets
hb_sound = pygame.mixer.Sound('./music/bullet.wav')
hb_sound.set_volume(2)

# music for destroying enemies
ed_sound = pygame.mixer.Sound('./music/enemy1_down.wav')
ed_sound.set_volume(5)

# music for destroying heroplane
hd_sound = pygame.mixer.Sound('./music/hpDown.wav')
hd_sound.set_volume(6)

# music for destroying boss
bDown = pygame.mixer.Sound('./music/bDown.wav')
bDown.set_volume(20)

# music for destroying missiles
mDown= pygame.mixer.Sound('./music/mDown.wav')
mDown.set_volume(5)
import os
import pygame
pygame.init()

images = [pygame.transform.scale(pygame.image.load(os.path.join("images", "bear1.png")), (64, 64)),
              pygame.transform.scale(pygame.image.load(os.path.join("images", "bear2.png")), (64, 64))]
imagesobs = [pygame.transform.scale(pygame.image.load(os.path.join("images", "goal.png")), (128, 128))]
             
SIZE = WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = pygame.Color('black')
FPS = 60

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Declare isJump as a global variable
global isJump
isJump = False
jumpCount = 10

class Basket(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Basket, self).__init__()

        size = (128, 128)  # Storleken på den förstorade bilden
        self.rect = pygame.Rect((750, 400), size)  # Skapa en rektangel för sprite-positionen och storleken
        self.images = image  # Lista med alla bilder för sprite-animationen
        self.index = 0  # Index för den aktuella bilden i animationen
        self.image = image[self.index]  # Aktuell bild som ska visas
        
        self.velocity = pygame.math.Vector2(-1, 0)  # Sprite-hastighet i x- och y-riktning

        self.animation_time = 0.2  # Tid mellan varje bildbyte i sekunder
        self.current_time = 0  # Aktuell tid sedan senaste bildbyte

    def update(self, dt):
        # Uppdatera sprite-tilståndet baserat på tidsskillnaden dt
        self.update_time_dependent(dt)
        if self.rect.x < -100:
            self.kill()  # Ta bort hindret från sprite-gruppen
            
            
        # Skriv ut x-koordinaten
        print("X-coordinate:", self.rect.x)

    def update_time_dependent(self, dt):
        # Uppdatera aktuell tid
        self.current_time += dt
        # Byt bild om det har gått tillräckligt med tid sedan förra bildbytet
        if self.current_time >= self.animation_time:
            self.current_time = 0  # Återställ tiden
            self.index = (self.index + 1) % len(self.images)  # Gå till nästa bild i sekvensen
            self.image = self.images[self.index]  # Uppdatera aktuell bild

        # Flytta sprite baserat på dess hastighet
        self.rect.move_ip(*self.velocity)



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super(AnimatedSprite, self).__init__()

        size = (128, 128)  # Storleken på den förstorade bilden
        self.rect = pygame.Rect((100, 450), size)  # Skapa en rektangel för sprite-positionen och storleken
        self.images = image  # Lista med alla bilder för sprite-animationen
        self.index = 0  # Index för den aktuella bilden i animationen
        self.image = image[self.index]  # Aktuell bild som ska visas
        
        self.velocity = pygame.math.Vector2(0, 0)  # Sprite-hastighet i x- och y-riktning

        self.animation_time = 0.2  # Tid mellan varje bildbyte i sekunder
        self.current_time = 0  # Aktuell tid sedan senaste bildbyte

    def update(self, dt):
        # Uppdatera sprite-tilståndet baserat på tidsskillnaden dt
        self.update_time_dependent(dt)
        

    def update_time_dependent(self, dt):
        # Uppdatera aktuell tid
        self.current_time += dt
        # Byt bild om det har gått tillräckligt med tid sedan förra bildbytet
        if self.current_time >= self.animation_time:
            self.current_time = 0  # Återställ tiden
            self.index = (self.index + 1) % len(self.images)  # Gå till nästa bild i sekvensen
            self.image = self.images[self.index]  # Uppdatera aktuell bild

        # Flytta sprite baserat på dess hastighet
        self.rect.move_ip(*self.velocity)

def main():
    global isJump  # Declare isJump as global within the function
   
    player = AnimatedSprite(image=images)
    basket = Basket(image=imagesobs)
    
    all_sprites = pygame.sprite.Group(basket, player)  # Lägg till både spelaren och hindret i sprite-gruppen

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Handle spacebar press for jumping
                    if not isJump:
                        isJump = True
                        jumpCount = 10

        if isJump:
            if jumpCount >= -10:
                neg = 1
                if jumpCount < 0:
                    neg = -1
                player.rect.y -= (jumpCount ** 2) * 0.5 * neg
                jumpCount -= 1
            else:
                isJump = False
                jumpCount = 10
                # Reset Y coordinate to initial Y coordinate
                player.rect.y = 450

        all_sprites.update(dt)  # Anropa update() med argument dt
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()

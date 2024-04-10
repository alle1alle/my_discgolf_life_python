import os
import pygame

pygame.init()

# Load images
images = [pygame.transform.scale(pygame.image.load(os.path.join("images", "bear1.png")), (64, 64)),
          pygame.transform.scale(pygame.image.load(os.path.join("images", "bear2.png")), (64, 64))]
imagesobs = [pygame.transform.scale(pygame.image.load(os.path.join("images", "goal.png")), (128, 128))]

# Load sound
jump_sound = pygame.mixer.Sound(os.path.join("sounds", "disc_jump.wav"))



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
    def __init__(self, image, x):
        super(Basket, self).__init__()

        size = (128, 128)  # Size of the enlarged image
        self.rect = pygame.Rect((x, 400), size)  # Create a rectangle for sprite position and size
        self.images = image  # List of all images for sprite animation
        self.index = 0  # Index for the current image in the animation
        self.image = image[self.index]  # Current image to display
        
        self.velocity = pygame.math.Vector2(-10, 0)  # Sprite velocity in x and y direction

        self.animation_time = 0.2  # Time between each image change in seconds
        self.current_time = 0  # Current time since last image change
        self.scored = False  # Flag to track whether the basket has been scored

    def update(self, dt):
        # Update sprite state based on the time difference dt
        self.update_time_dependent(dt)
        if self.rect.x < -100:
            self.kill()  # Remove the obstacle from the sprite group

    def update_time_dependent(self, dt):
        # Update current time
        self.current_time += dt
        # Change image if enough time has passed since the last image change
        if self.current_time >= self.animation_time:
            self.current_time = 0  # Reset the time
            self.index = (self.index + 1) % len(self.images)  # Go to the next image in the sequence
            self.image = self.images[self.index]  # Update current image

        # Move sprite based on its velocity
        self.rect.move_ip(*self.velocity)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super(AnimatedSprite, self).__init__()

        size = (128, 128)  # Size of the enlarged image
        self.rect = pygame.Rect((100, 450), size)  # Create a rectangle for sprite position and size
        self.images = image  # List of all images for sprite animation
        self.index = 0  # Index for the current image in the animation
        self.image = image[self.index]  # Current image to display
        
        self.velocity = pygame.math.Vector2(0, 0)  # Sprite velocity in x and y direction

        self.animation_time = 0.2  # Time between each image change in seconds
        self.current_time = 0  # Current time since last image change

    def update(self, dt):
        # Update sprite state based on the time difference dt
        self.update_time_dependent(dt)

    def update_time_dependent(self, dt):
        # Update current time
        self.current_time += dt
        # Change image if enough time has passed since the last image change
        if self.current_time >= self.animation_time:
            self.current_time = 0  # Reset the time
            self.index = (self.index + 1) % len(self.images)  # Go to the next image in the sequence
            self.image = self.images[self.index]  # Update current image

        # Move sprite based on its velocity
        self.rect.move_ip(*self.velocity)

def display_score(score):
    font = pygame.font.SysFont("Kristen ITC", 36)
    text = font.render("Score: " + str(score), True, pygame.Color('white'))
    text_rect = text.get_rect(center=(WIDTH // 10, HEIGHT // 2))
    screen.blit(text, text_rect)

def main():
    global isJump  # Declare isJump as global within the function
    global score

    player = AnimatedSprite(image=images)
    baskets = []  # List to hold multiple basket instances
    basket_spawn_time = 2  # Time interval to spawn a new basket (in seconds)
    spawn_timer = basket_spawn_time  # Timer to keep track of when to spawn a new basket
    x_offset = 150  # X offset between consecutive baskets
    initial_x = 750  # Initial x position of the first basket
    score = 0  # Player's score

    all_sprites = pygame.sprite.Group(player)  # Add player to sprite group

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
                        # Play jump sound
                        jump_sound.play()

        if isJump:
            if jumpCount >= -10:
                neg = 1
                if jumpCount < 0:
                    neg = -1
                player.rect.y -= (jumpCount ** 2) * 0.5 * neg
                jumpCount -= 0.8
            else:
                isJump = False
                jumpCount = 10
                # Reset Y coordinate to initial Y coordinate
                player.rect.y = 450

        # Update spawn timer
        spawn_timer -= dt
        if spawn_timer <= 0:
            # Spawn a new basket
            basket = Basket(image=imagesobs, x=initial_x)
            baskets.append(basket)
            all_sprites.add(basket)
            # Reset spawn timer
            spawn_timer = basket_spawn_time
            # Adjust initial_x for the next basket
            initial_x += x_offset

        # Check for collisions between player and baskets
        for basket in baskets:
            if basket.rect.left < player.rect.right and not basket.scored:
                basket.scored = True
                score += 1
                print("Score:", score)

        all_sprites.update(dt)  # Call update() with argument dt
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)

        # Display score
        display_score(score)

        pygame.display.update()




if __name__ == '__main__':
    main()

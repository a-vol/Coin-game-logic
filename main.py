'''
Some basic game logic for a coin game

'''
import pygame
import random # for generating random coordinates of the coin
import math # used to calculate the distance between the player and the coin 

#Initialising pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Test')
clock = pygame.time.Clock()

#Colours
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

#Defining a class or a template for coins
class Coin:
    #Defining the constants of a coin, each coin has radius of 10, colour of GOLD and value of 10
    radius = 10
    color = GOLD
    value = 10
    

    def __init__(self, center):
        #This __init__() part is called a constructor, it takes the coordinates of the center of the coin 
        # Don't worry about the self parameter its just part of object oriented programming
        self.center = center

    def draw(self):# This draws the coin on the screen
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    def check_collision(self, player_Rect): # The math here is a bit complex
        '''
        Basically, it calculates the distance between the center of the coin
        and the closest x and y coordinate of the player rectangle, then it calculates
        the actual distance using pythagoras theorem, then 
        if the distance is smaller than the radius, the player is either touching or overlapping
        therefore collided.
        
        '''
        closest_x = max(player_Rect.x, min(self.center[0], player_Rect.x + player_Rect.width))
        closest_y = max(player_Rect.y, min(self.center[1], player_Rect.y + player_Rect.height))
        distance = math.hypot(self.center[0] - closest_x, self.center[1] - closest_y)
        if distance < self.radius:
            return True
        else:
            return False
        
    
        
#Defining a class or a template for the player
class Player:
    #Defining the constants of the player
    player_width = 20
    player_height = 50
    score = 0
    speed = 4 #This is just how fast/slow the player moves in every direction

    def __init__(self, x, y):
        #And again, every class must have a constructor, which initalises the data of an object of that class
        self.rect = pygame.Rect(x, y, self.player_width, self.player_height)
        self.color = (0, 0, 0)

    def draw(self, screen):# This draws the player on the screen
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, keys):
        # This section takes in a list of the keys pressed by the player
        #If the key is pressed, the player moves in that direction, for here ive used WASD as the movement keys
        #The and statements are just to prevent the player from going out of the screen
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < 600 - self.player_height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < 800 - self.player_width:
            self.rect.x += self.speed
            
    def update_score(self, value, text_file): 
        # This updates the score in the current game, and then updates the score in the actual file
        self.score += value
        with open(text_file, 'r') as file:
            try:
                current_score = int(file.read())
            except ValueError:
                current_score = 0
            
        new_Score = current_score + value
        with open(text_file, 'w+') as file:
            file.write(str(new_Score))
        
    def display_score(self):
        # This displays the score on the screen
        font = pygame.font.SysFont(None, 24)
        text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(text, (10, 10))
        
        
    
def generate_random_coordinates():
    # This generates random coordinates for the coins
    # Normally you would put the ranges as 0, to heigh/width of the screen
    # However the logic just ensures no coin is 'half in the screen'
    x = random.randint(0 + Coin.radius, 800 - Coin.radius,)
    y = random.randint(0 + Coin.radius, 600 - Coin.radius)
    coordinates = (x, y)
    return coordinates

#Defining a list of coins
Coins = []
# Here, we are saying, create 8 coins with random coordinates and add them to the list
# The formal way of saying it is, we 'instantiate' 8 'objects' of the Coin class
# In OOP, each object is called an instance, and each coin in the list is unique, for example each coin has 
# its own x and y coordinate
for i in range (8):
    coin = Coin(generate_random_coordinates())
    Coins.append(coin)

# Defining the player with starting coordinates
player = Player(400, 300)


def main():

    # Just initialising the scores file
    # Also checks if the file exists, if not, it creates it
    scores_txt = 'scores.txt'
    with open(scores_txt, 'a') as file:
        file.write('')

    running = True
    while running:

        screen.fill(WHITE)

        # Simple event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Here we draw every coin in the list of coins
        for coin in Coins:
            coin.draw() 
            # This is an example calling the draw method of the coin class
            # Each coin is unique, and each coin has the ability to 'draw' itself 
            # So if you have 8 coins, each coin will draw itself, so 8 coins are drawn
            if coin.check_collision(player.rect):
                # Another example of how object oriented programming ( OOP ) works
                # Earlier we defined a method in the coin class called check_collision 
                # And each coin is unique, so each coin is able to compare its own values with the player values
                Coins.remove(coin)
                # If detection is True, the coin is removed from the list
                # In the next loop, or iteration, the coin will not be drawn, hence disappearing
                player.update_score(coin.value, scores_txt)

        # This section handles the player movement
        keys = pygame.key.get_pressed()
        player.draw(screen)
        player.move(keys)

        player.display_score()
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
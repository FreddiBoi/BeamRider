#Module 13 Final Game Assignment 
#Fred Doersam
import pygame
import time
from pygame.locals import *
from pygame import mixer
pygame.init()
# Colours to use for the window
BLACK = (0, 0, 0)
#Player 1's trail colour which is blue
P1_COLOUR = (0, 255, 255) 
#Player 2's trail colour which is orange
P2_COLOUR = (255,165,0)  
#Setting a variable to check if the program is in the main menu or not
main_menu = True
#Pause is set to false 
pause = False
#Controls is set to false
controls = False

#Setting a variable to check if the user clicked Start, Controls, Main_menu, or Pause, or if the game has ended
clicked = False
#Creating a font for all text in the game (font style, font size) 
font = pygame.font.SysFont('impact', 36)
pygame.display.set_caption("Main Menu")
#Defining the colours for the main menu White, Black, Yellow, Blue(uses RGB values to make colours)
#RGB is how much of either Red, Blue or Green a colour has, the higher the number the higher the saturation
White = (255,255,255)
Black = (0,0,0)
Yellow = (255,255,0)
Blue = (0,0,255)
Green = (0,255,0)
Red = (255,0,0)
#Height of the window = 800
Width = 800
#Width of the window = 700
Height = 700
screen = pygame.display.set_mode((Width, Height))
gameDisplay = pygame.display.set_mode((Width, Height))

#All the buttons throughout the GUI with their hover imgs aswell, including start, menu, title, main menu, pause, controls, play, and back.
#All of these buttons are converted to the size that I needed them to be by using pygame.transform.scale. 
start_img = pygame.image.load('Start_img.png').convert_alpha()
start_img = pygame.transform.scale(start_img,(400, 150))
hover_img = pygame.image.load('Start_img2.png').convert_alpha()
hover_img = pygame.transform.scale(hover_img,(400, 150))
menu_bg = pygame.image.load('BeamRider.png').convert_alpha()
menu_bg = pygame.transform.scale(menu_bg,(800,600))
title_img = pygame.image.load('Title.png').convert_alpha()
title_img = pygame.transform.scale(title_img,(785, 150))
Mainmenu_img = pygame.image.load('Main_menu.png').convert_alpha()
Mainmenu_img = pygame.transform.scale(Mainmenu_img,(150, 50))
hovermenu_img = pygame.image.load('Main_menu1.png').convert_alpha()
hovermenu_img = pygame.transform.scale(hovermenu_img,(150, 50))
Pause_img = pygame.image.load('Pause.png').convert_alpha()
Pause_img = pygame.transform.scale(Pause_img,(150, 40))
Pause1_img = pygame.image.load('Pause1.png').convert_alpha()
Pause1_img = pygame.transform.scale(Pause1_img,(150, 40))
Pause_bg = pygame.image.load('Pause_bg.png').convert_alpha()
Pause_bg = pygame.transform.scale(Pause_bg,(800, 800))
Controls_img = pygame.image.load('Controls_img.png').convert_alpha()
Controls_img = pygame.transform.scale(Controls_img,(245, 125))
Controls_hover = pygame.image.load('Controls_hover1.png').convert_alpha()
Controls_hover = pygame.transform.scale(Controls_hover,(245, 125))
Play_hover = pygame.image.load('Continue_hover.png').convert_alpha()
Play_hover = pygame.transform.scale(Play_hover,(400, 150))
Play = pygame.image.load('Continue.png').convert_alpha()
Play = pygame.transform.scale(Play,(400, 150))
Back = pygame.image.load('Back.png').convert_alpha()
Back = pygame.transform.scale(Back,(150, 100))
Back_hover = pygame.image.load('Backhover.png').convert_alpha()
Back_hover = pygame.transform.scale(Back_hover,(150, 100))
#Defining a function named draw_text that draws the text and font on the coordinate plane 
def draw_text(text, font, text_col, x, y,):    
    
    #Setting a variable as the text that is given and renders is with a given colour
    img = font.render(text, True, text_col)

    #Draws the text on the display window
    screen.blit(img, (x, y))
    
#Creates a class for the button in regards to the location, size and if it is clicked or not
class MenuButton():

    #This function is the creation of the button itself, it's called when the class is called
    def __init__(self, x, y, image):
        #Sets the button's image to the given image
        self.image = image

        #Sets a rectangle to be the size of the image size(width x height). used for mouse detection
        self.rect = self.image.get_rect()

        #Sets the x and y coordinates of the rectangle to the given values on lines 140 - 142
        self.rect.x = x
        self.rect.y = y

        #Setting a variable to check if a button is clicked or not
        self.clicked = False
       
   
    #This function checks for cursor collision as well as draws the button onto the window
    def draw(self, image, image2):

        #Creating a variable for returning an action by the mouse to the main program
        action = False

        #Gets the mouse position, sets it to a variable named pos
        pos = pygame.mouse.get_pos()

        #Checks if the mouse is hovering over the button
        if self.rect.collidepoint(pos):
            #If the mouse is on the button, set the image to the hover image
            self.image = image 

            #Checks if the mouse is clicked and if it isnt already clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

                #Sets the action to return and that the mouse has been clicked as true
                action = True
                self.clicked = True
        
        #If mouse is not over button, it will then set the image to the original button image unaltered
        else:
            self.image = image2        

        #Checks if the mouse isn't pressed
        if pygame.mouse.get_pressed()[0] == 0:
            #Sets the click variable as false so the computer knows its not pressed
            self.clicked = False
        

        #Drawing the button
        screen.blit(self.image, self.rect)

        #Returns the value of action
        return action

#Creating player class
class Player:
    #Init method for the player class
    def __init__(self, x, y, b, c):
        #The players x coord
        self.x = x  
        #The players y coord
        self.y = y  
        #The players speed
        self.speed = 1  
        #The players direction
        self.bearing = b  
        #The players colour
        self.colour = c
        #Setting boost to false
        self.boost = False  
        #Controls how long the boost is
        self.start_boost = time.time() 
        self.boosts = 3
        #The players rect object
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  
    
    #Method to draw self
    def __draw__(self):
        
        #This redefines the rect
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2) 
        #This draws the player onto the screen 
        pygame.draw.rect(screen, self.colour, self.rect, 0)  
    #Method for moving the player
    def __move__(self):
        
        #Checking that the player isnt currently boosting
        if not self.boost:  
            self.x += self.bearing[0]
            self.y += self.bearing[1]
        else:
            self.x += self.bearing[0] * 2
            self.y += self.bearing[1] * 2
    #Method for boosting the player
    def __boost__(self):
        
        #If the boost is true activate time.time()
        if self.boosts > 0:
            self.boosts -= 1
            self.boost = True
            self.start_boost = time.time() 


#Starting a new game function 
def new_game():
    new_p1 = Player(50, 250, (2, 0), P1_COLOUR)
    new_p2 = Player(width - 50, 400, (-2, 0), P2_COLOUR)
    #Returns p1 and p2 
    return new_p1, new_p2


#Window dimensions again for game not menu
width = 800
height = 600
#The space at top of window that shows the score and main menu and pause button
offset = height / width  + 60
#Creates the window
screen = pygame.display.set_mode((width, height))  
#Sets the window title to BeamRider
pygame.display.set_caption("BeamRider")  
#Regulates the FPS
clock = pygame.time.Clock() 
#Used to check if a collision between rects occured
check_time = time.time()  
#A list of all the players objects
objects = list() 
#A list of all the player trail rects in the game
path = list() 
#Creates the starting player with placement and colour
p1 = Player(50, (height- offset) / 2, (2, 0), P1_COLOUR)  
#Creates the second starting player with placement and colour
p2 = Player(width - 50, (height- offset) / 2, (-2, 0), P2_COLOUR)
objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))


#The players scores at the start of the game. -1 because if [0, 0], player 2 would start with 1 point.
player_score = [0, -1]  
#The outside walls of the window
wall_rects = [pygame.Rect([0, offset, 15, height]) , pygame.Rect([0, offset, width, 15]),\
              pygame.Rect([width - 15, offset, 15, height]),\
              pygame.Rect([0, height - 15, width, 15])]  

#Done is set = to false               
done = False
#New is set = to false
new = False
#Drawing the buttons and declaring the position on the screen where I want them to be.
Start_btn = MenuButton(190,260, start_img) 
main_btn = MenuButton(50, 5, Mainmenu_img)
pause_btn = MenuButton(580, 15, Pause_img)
controls_btn = MenuButton(265, 431, Controls_img)
Play_btn = MenuButton(200, 230, Play)
Back_btn = MenuButton(620, 20, Back)
while not done:
    #If main_menu = true, the menu background and title are put onto the screen
    if main_menu == True:
        screen.blit(menu_bg,(0,0)) 
        screen.blit(title_img,(0,0))
        
        #If start button is clicked then main menu = false and the game begins
        if Start_btn.draw(hover_img, start_img): 
            main_menu = False
           
    #If controls is clicked then the function controls = true and main_menu = true so the game dopesnt start
    if controls_btn.draw(Controls_hover, Controls_img):
            controls = True
            main_menu = True
    #If pause is clicked then main_menu = true so game pauses, and pause background covers the whole screen     
    if pause ==True:
        main_menu = True
        screen.blit(Pause_bg,(0,0))
        #If Play is clicked then pause = false and main menu = false so the game starts again
        if Play_btn.draw(Play_hover, Play):
                pause = False
                main_menu = False
    #If controls is clicked then main_menu = true so game doesn't start, and the pause bg is put onto the screen
    if controls == True:
        main_menu = True
        screen.blit(Pause_bg,(0,0))
        #Draws text to the screen to tell the user the controls for player 1 and 2, and tells the user the aim of the game. Using font, colour, and position
        draw_text("CONTROLS:", font, BLACK, 20, 30)
        draw_text("1ST PLAYER (WASD)   'LEFT SHIFT TO BOOST'", font, P1_COLOUR, 20, 80)
        draw_text("2ND PLAYER (ARROW KEYS)   'RIGHT SHIFT TO BOOST'", font, P2_COLOUR, 20, 120)
        draw_text("Aim Of The Game:", font, Black, 20, 160)
        draw_text("The aim of the game is to avoid the wall barriers", font, (230,230,250), 20, 200)
        draw_text("marked in blue and the opponent's trail, which is", font, (230,230,250), 20, 240)
        draw_text("either player one or twos colour. Using (wasd) and", font, (230,230,250), 20, 280)
        draw_text("left shift for player 1, and (arrow keys) and right shift", font, (230,230,250), 20, 320)
        draw_text("for player two your goal is to move up, right, left, and", font, (230,230,250), 20, 360)
        draw_text("down to traverse across the playfield to kill the other", font, (230,230,250), 20, 400)
        draw_text("player. You can use shift to boost or go through the", font, (230,230,250), 20, 440)
        draw_text("opponent's walls, but be aware that there is a 50", font, (230,230,250), 20, 480)
        draw_text("percent chance you will hit their wall.", font, (230,230,250), 20, 520)
        #If back button is clicked then main menu is true and controls is false
        if Back_btn.draw(Back_hover, Back):
            main_menu = True
            controls = False
        


    if main_menu == False: 
        
        
        #Checks for all the events in the last tick
        for event in pygame.event.get(): 
            #Checks if closed button was pressed
            if event.type == pygame.QUIT:  
                done = True

            #Checking if a key has been pressed. Also making it so if the player is going up they can't go down to make sure they can not eliminate themself
            elif event.type == pygame.KEYDOWN: 
                if objects[0].bearing != (0, 2):
                    #Player 1s keys (wasd)
                    if event.key == pygame.K_w:
                        objects[0].bearing = (0, -2)
                if objects[0].bearing != (0, -2):
                    if event.key == pygame.K_s:
                        objects[0].bearing = (0, 2)
                if objects[0].bearing != (2, 0):
                    if event.key == pygame.K_a:
                        objects[0].bearing = (-2, 0)
                if objects[0].bearing != (-2, 0):
                    if event.key == pygame.K_d:
                        objects[0].bearing = (2, 0)
                if event.key == pygame.K_TAB:
                        objects[0].__boost__()
                    # Player 2s keys (up, right, down, left) 
                if objects[1].bearing != (0,2):
                    if event.key == pygame.K_UP:
                        objects[1].bearing = (0, -2)
                if objects[1].bearing != (0, -2):
                    if event.key == pygame.K_DOWN:
                        objects[1].bearing = (0, 2)
                if objects[1].bearing != (2, 0):
                    if event.key == pygame.K_LEFT:
                        objects[1].bearing = (-2, 0)
                if objects[1].bearing != (-2, 0):
                    if event.key == pygame.K_RIGHT:
                        objects[1].bearing = (2, 0)
                if event.key == pygame.K_RSHIFT:
                        objects[1].__boost__()
    # Clears the screen and makes it black
        screen.fill(BLACK)  
        # If main_menu is clicked then main_menu = true and player score is reset
        if main_btn.draw(hovermenu_img, Mainmenu_img):
            main_menu = True
            player_score = [0, 0]  
        #If pause is clicked then the pause function = true 
        if pause_btn.draw(Pause1_img, Pause_img):
            pause = True

        #Draws the walls in making sure that its shorter at the top
        for r in wall_rects: pygame.draw.rect(screen, (0, 150, 230), r, 0)  
        #Limits how long the player can boost to 0.5s
        for o in objects:
            if time.time() - o.start_boost >= 0.5:  
                o.boost = False
            #Collided with path or wall
            if (o.rect, '1') in path or (o.rect, '2') in path \
            or o.rect.collidelist(wall_rects) > -1:  
                #Prevents the player from hitting the path they just made by setting the time to 0.1
                if (time.time() - check_time) >= 0.1:
                    check_time = time.time()

                    if o.colour == P1_COLOUR:
                        player_score[1] += 1
                    else: player_score[0] += 1
                    # Setting new = to true so the game runs after a death
                    new = True
                    new_p1, new_p2 = new_game()
                    objects = [new_p1, new_p2]
                    path = [(p1.rect, '1'), (p2.rect, '2')]
                    break
            else: 
                path.append((o.rect, '1')) if o.colour == P1_COLOUR else path.append((o.rect, '2'))
            #Running the draw function and move function
            o.__draw__()
            o.__move__()

        for r in path:
            if new is True:
                #Empties the path
                path = []
                #New = to false
                new = False
                break
            if r[1] == '1': pygame.draw.rect(screen, P1_COLOUR, r[0], 0)
            else: pygame.draw.rect(screen, P2_COLOUR, r[0], 0)
        
        #Displays the current score on the screen in the offest
        score_text = font.render('{0} : {1}'.format(player_score[0], player_score[1]), 1, (255, 153, 51))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = int(width / 2)
        score_text_pos.centery = int(offset / 2)     
        screen.blit(score_text, score_text_pos)


    for event in pygame.event.get(): 
        #Checks if the QUIT button was pressed
        if event.type == pygame.QUIT:  
            #DOne is set to true
            done = True


    #Doesn't update the whole screen but a portion of it 
    pygame.display.flip()  
    #Regulates the frames per second
    clock.tick(60) 
#Closing the window function is set
pygame.quit()
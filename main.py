import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from figure import *
from tkinter import *
from tkinter import ttk
from tkinter import Radiobutton, IntVar
import time
import serial
import threading
import re
import random

ApplicationGL = False

class PortSettings:
    Name = "COM5"
    Speed = 19200
    Difficulty = 0
    Timeout = 2
class IMU:
    Roll = 0
    roll_error = 0
    Pitch = 0
    pitch_error = 0
    Yaw = 0

class Background:
    r = 0
    g = 0
    b = 0
    score = 0
    start_time = 0
    ####Adjustable####
    timer = 60
    rollover_time = 0
    
    #Used so after update period is over, error will only be updated once
    #Can't be 0
    error_timer = 1
    error_delay = 10
    error = 0

    ####Adjustable####
    total_moves = 30
    moves = 0


    #Changes private variables r, g, and b
    def randomizeBackground(self):
        self.r = round(random.uniform(0, 1), 1)
        self.g = round(random.uniform(0, 1), 1)
        self.b = round(random.uniform(0, 1), 1)

    #Changes private member variable start_time
    def start_timer(self):
        self.start_time = time.time()

    #Returns time left
    def check_timer(self):
        elapsed_time = time.time() - self.start_time
        #The max safegaurds it from showing as a negative number on screen
        if myport.Difficulty == 4:
            return max(0, (self.timer + self.rollover_time) - int(elapsed_time))
        else:
            return max(0, self.timer - int(elapsed_time))

    #Extra time from previous round transfers over
    def add_rollover_time(self):
        elapsed_time = time.time() - self.start_time
        self.rollover_time = max(0, self.timer - int(elapsed_time))
    
    #Changes private variable error
    def update_error(self):
        elapsed_time = round(time.time() - self.start_time)
        if(self.error_timer != elapsed_time):
            self.error_timer = elapsed_time
            self.error = 10 * round(abs(background.r-color_factor.r) + abs(background.g-color_factor.g) + abs(background.b-color_factor.b), 1)
    
    #Returns moves left
    def check_moves(self):
        return self.total_moves-self.moves
    
    def init(self):
        prev = (self.r, self.b, self.g)
        self.randomizeBackground()
        #If it randomizes to the starting color or to previous color, reroll
        while ((self.r, self.b, self.g) == prev):
            self.randomizeBackground()
        #Stores the new starting time
        self.start_timer()
        #Find error at start
        self.update_error()

        self.moves = 0


#Background keeps most of the game data
background = Background()

class ColorFactor:
    #R, G, and B must be between 0 and 1
    r = 0.5
    g = 0.5
    b = 0.5
    ####Adjustable####
    change_amount = 0.1

    #Stores chars representing the different orientations
    #Will be compared with current orientation to see if color should be changed
    #Increasing and decreasing share the same char because it's impossible to get from increase to decrease without going through another orientation
    prev = 'c'
    #stores amount of time in a given orientation
    time = 0
    
    #RGB = (0.5, 0.5, 0.5)
    def reset_colors(self):
        self.r = 0.5
        self.g = 0.5
        self.b = 0.5

    #Change color based on orientation and time count
    def color_handler(self):
        roll = myimu.Roll
        pitch = myimu.Pitch
        ####ADJUSTABLE####
        #How far the roll must be to be considered in a different direction
        roll_bound = 20
        #####ADJUSTABLE####
        #How far the pitch must be to be considered in a different direction
        pitch_bound = 10
        ####ADJUSTABLE####
        #The amount of time you need to be in a certain direction before changing RGB
        time_bound = 40

        ####ADJUSTABLE####
        #Make darken and lighten less sensitive
        side_bound = 8

        ####RIGHT####
        #Increase all if right
        #Blue if right diagonal
        if(pitch < -1*pitch_bound):
            #Decrease blue
            if(-roll_bound+side_bound > roll):
                #If previous color was blue
                if(self.prev == 'b'):
                    #Increment timer
                    self.time+=1
                    #If waited long enough
                    if(self.time%time_bound == 0):
                        self.update_color('b', 0)
                else:
                    #Reset timer and switch colors
                    self.prev = 'b'
                    self.time = 0
                
            #Increase blue
            elif(roll_bound-side_bound < roll):
                if(self.prev == 'b'):
                    self.time+=1
                    if(self.time%time_bound == 0):
                        self.update_color('b', 1)
                else:
                    self.prev = 'b'
                    self.time = 0
            #Increase brighness
            else:
                if(self.prev == 'w'):
                    self.time+=1
                    if(self.time%(round(time_bound*1.5)) == 0):
                        self.update_color('w', 1)
                else:
                    self.prev = 'w'
                    self.time = 0

        ####LEFT####
        #Decrease all if left
        #Red if left diagonal
        elif(pitch > pitch_bound):
            if(-roll_bound+side_bound > roll):
                if(self.prev == 'r'):
                    self.time+=1
                    if(self.time%time_bound == 0):
                        self.update_color('r', 0)
                else:
                    self.prev = 'r'
                    self.time = 0
                
            #Increase red
            elif(roll_bound-side_bound < roll):
                if(self.prev == 'r'):
                    self.time+=1
                    if(self.time%time_bound == 0):
                        self.update_color('r', 1)
                else:
                    self.prev = 'r'
                    self.time = 0
            #Decrease brighness
            else:
                if(self.prev == 'w'):
                    self.time+=1
                    if(self.time%(round(time_bound*1.5)) == 0):
                        self.update_color('w', 0)
                else:
                    self.prev = 'w'
                    self.time = 0
                
        ####CENTER####
        #Green if tilted
        #Nothing if centered
        else:
            #Decrease green
            if(-roll_bound > roll):
                if(self.prev == 'g'):
                    self.time+=1
                    if(self.time%time_bound == 0):
                        self.update_color('g', 0)
                else:
                    self.prev = 'g'
                    self.time = 0
                
            #Increase green
            elif(roll_bound < roll):
                if(self.prev == 'g'):
                    self.time+=1
                    if(self.time%time_bound == 0):
                        self.update_color('g', 1)
                else:
                    self.prev = 'g'
                    self.time = 0
            #If it is neither, then it is stationary. Don't change RGB and reset timer
            else:
                self.prev = 'c'
                self.time = 0

    def update_color(self, color, increase):
        
        #Don't update color if difficulty = 0
        if myport.Difficulty == 0:
            return
        
        change_amount = self.change_amount
        if(increase == 0):
            change_amount *= -1
        
        oldr = (self.r, self.g, self.b)
        
        #Never goes above 1 or below 0
        if color == 'r':
            self.r = round(max(0, min(1, self.r + change_amount)), 1)
        elif color == 'g':
            self.g = round(max(0, min(1, self.g + change_amount)), 1)
        elif color == 'b':
            self.b = round(max(0, min(1, self.b + change_amount)), 1)
        elif color == 'w':
            self.r = round(max(0, min(1, self.r + change_amount)), 1)
            self.g = round(max(0, min(1, self.g + change_amount)), 1)
            self.b = round(max(0, min(1, self.b + change_amount)), 1)
        else:
            print("Unknown character")

        #If colors were changedpy, a move was done
        if oldr != (self.r, self.g, self.b):
            background.moves += 1

    def compareBackground(self):
        if(background.r == self.r and background.g == self.g and background.b == self.b):
            return True
        else:
            return False

    def explainAction(self):
        match self.prev:
            case 'r':
                if myimu.Roll > 0:
                    return "Adding Red   "
                else:
                    return "Removing Red "
            case 'g':
                if myimu.Roll > 0:
                    return "Adding Green "
                else:
                    return "Remove Green "
            case 'b':
                if myimu.Roll > 0:
                    return "Adding Blue  "
                else:
                    return "Removing Blue"
            case 'w':
                #Right
                if myimu.Pitch < 0:
                    return "Brightening  "
                #Left
                else:
                    return "Darkening    "
            case _:
                    return "             "


#My port is used for initializations and to connect IMU with PySerial
myport = PortSettings()
#Keeps track of pitch, roll, and yaw values
myimu  = IMU()
#Keeps track of color changes
color_factor = ColorFactor()



#Ask for correct port and speed for serial communication. Once entered, program can start
def RunAppliction():
    global ApplicationGL
    #Get entries from the start screen
    myport.Name = Port_entry.get()
    myport.Speed = Baud_entry.get()
    myport.Difficulty = Difficulty_entry.get()
    #Get difficulty

    #Start now
    ApplicationGL = True
    ConfWindw.destroy()

#Beginning screen to ask for port number and speed
ConfWindw = Tk()
ConfWindw.title("Configure Settings")
ConfWindw.configure(bg = "#2E2D40") 
ConfWindw.geometry('300x280')
ConfWindw.resizable(width=False, height=False)
positionRight = int(ConfWindw.winfo_screenwidth()/2 - 300/2)
positionDown = int(ConfWindw.winfo_screenheight()/2 - 150/2)
ConfWindw.geometry("+{}+{}".format(positionRight, positionDown))

# Title label
title_label = Label(text="3D Color Match", font=("", 18, "bold"), justify="center", bg="#2E2D40", fg="#FFFFFF")
title_label.place(x=150, y=20, anchor="center")

Port_label = Label(text = "Port:",font =("",12),justify= "right",bg = "#2E2D40",fg = "#FFFFFF")
Port_label.place(x = 65, y = 70,anchor = "center")
Port_entry = Entry(width = 20,bg = "#37364D", fg = "#FFFFFF", justify = "center")
Port_entry.insert(INSERT,myport.Name)
Port_entry.place(x = 180, y =70,anchor = "center")

Baud_label = Label(text = "Speed:",font =("",12),justify= "right",bg = "#2E2D40",fg = "#FFFFFF")
Baud_label.place(x = 55, y =120,anchor = "center")
Baud_entry = Entry(width = 20,bg = "#37364D", fg = "#FFFFFF", justify = "center")
Baud_entry.insert(INSERT,str(myport.Speed))
Baud_entry.place(x = 180, y = 120,anchor = "center")

Difficulty_label = Label(text="Difficulty:", font=("", 12), justify="right", bg="#2E2D40", fg="#FFFFFF")
Difficulty_label.place(x=51, y=178, anchor="center")

# Create a variable to store the selected difficulty
Difficulty_entry = IntVar()
Difficulty_entry.set(myport.Difficulty)  #Set the initial value to the default difficulty

#Switch buttons for difficulty selection
for i in range(1, 6):
    if (i == 1):
        button = Radiobutton(
        ConfWindw,
        text=str("T"),
        variable=Difficulty_entry,
        value=i,
        indicatoron=0,  #0 = circular button
        width=2,  
        height=2,  
        bd=4,  # Border width
        relief="raised",  #Button relief style
        bg="#2E2D40",  #Background color
        fg="#FFFFFF",  #Text color
        selectcolor="#135EF2",
        #Lambda function passes the current value
        command=lambda i=i: Difficulty_entry.set(i),
        )
    else: 
        button = Radiobutton(
            ConfWindw,
            text=str(i-1),
            variable=Difficulty_entry,
            value=i,
            indicatoron=0,  #0 = circular button
            width=2,  
            height=2,  
            bd=4,  # Border width
            relief="raised",  #Button relief style
            bg="#2E2D40",  #Background color
            fg="#FFFFFF",  #Text color
            selectcolor="#135EF2",
            #Lambda function passes the current value
            command=lambda i=i: Difficulty_entry.set(i),
        )
    button.place(x=85+ i * 33, y=178, anchor="center")

ok_button = Button(text = "Ok",width = 8,command = RunAppliction,bg="#135EF2",fg ="#FFFFFF")
ok_button.place(x = 145, y = 250,anchor="center")


#PyGame initialization and window (display new window)
def InitPygame():
    global display
    #Initialize
    pygame.init()
    #Display size
    display = (640,480)
    #DOUBLEBUF prevents flickering
    #PyGame will display on OpenGL (graphics interfect)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    #Name of the program (top left)
    pygame.display.set_caption('3D Color Match')


#Initialize OpenGL
def InitGL():
    #Initilaize game
    background.init()
    if myport.Difficulty != 0:
        glClearColor((background.r),(background.g),(background.b),1)
    else:
        glClearColor((1.0/255*46),(1.0/255*45),(1.0/255*64),1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    gluPerspective(100, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)

#Initialize OpenGL
def RestartGL():
    #Initilaize game
    background.init()
    background.score = 0
    background.rollover_time = 0
    if myport.Difficulty != 0:
        glClearColor((background.r),(background.g),(background.b),1)
    else:
        glClearColor((1.0/255*46),(1.0/255*45),(1.0/255*64),1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    gluPerspective(100, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)


#Text Writing Function
def DrawText(textString): 
    font = pygame.font.SysFont ("Courier New",25, True)
    #Parameters: text, true, color, background
    textSurface = font.render(textString, True, (255,255,0), (46,45,64,255))
    
    #Converts the image of the text into a bits of the string  
    textData = pygame.image.tostring(textSurface, "RGBA", True)   
    #Displays the bitfield at the bottom of the screen
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)    

#Make 3d Board
def DrawBoard():
    
    glBegin(GL_QUADS)
    x = 0
    
    color_factor.color_handler()
    

    for surface in surfaces:
        
        for vertex in surface:

            if x == 1:
                glColor3fv((color_factor.r, color_factor.g, color_factor.b))
            #For tutorial, show which direction changes which colors
            elif(myport.Difficulty == 1 and (x == 4 or x == 5)):
                match color_factor.prev:
                    case 'r':
                        glColor3fv((1, 0, 0))
                    case 'g':
                        glColor3fv((0, 1, 0))
                    case 'b':
                        glColor3fv((0, 0, 1))
                    case 'w':
                        #Right
                        if myimu.Pitch < 0:
                            #Whiter
                            glColor3fv((0.7, 0.7, 0.7))
                        #Left
                        else:
                            #Darker
                            glColor3fv((0.3, 0.3, 0.3))
                    case _:
                        glColor3fv(colors[x])
            else:
                glColor3fv(colors[x])
                

                      
            glVertex3fv(vertices[vertex])
        x += 1
    glEnd()

#Update entire GL World
def DrawGL():

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #Reset transformations
    glLoadIdentity() 
    gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
    #Depth perception
    glTranslatef(0.0,0.0, -5)   

    #Rotate camera by updating pitch and roll
    #Pitch and Roll are given in degrees (if pitch = 90, will rotate 90 degrees)
    #Parameters are angle, x, y, and z
    glRotatef(round(myimu.Pitch,1), 0, 0, 1)
    glRotatef(round(myimu.Roll,1), -1, 0, 0)

    #Print RGB and other info on screen
    match myport.Difficulty:
        #Tutorial Mode: Given the answer key and instructions
        case 1:
            DrawText("Red:{} Green:{} Blue:{}  {} {{{} {} {}}}".format(round(color_factor.r*10), round(color_factor.g*10), round(color_factor.b*10), color_factor.explainAction(), round(background.r*10), round(background.g*10), round(background.b*10)))
        
        #Given how far away (updates every 10 seconds)
        case 2:
            #If start or 5 seconds have passed
            if(round(time.time()-background.start_time, 1)%background.error_delay == 0):
                
                background.update_error()
            DrawText("R:{} G:{} B:{}       Error: {}      Update: {}".format(round(color_factor.r*10), round(color_factor.g*10), round(color_factor.b*10), round(background.error), background.error_delay - round(time.time()-background.start_time)%background.error_delay))
        
        #Regular Game
        case 3:
            DrawText("R:{} G:{} B:{}            Elapsed Time: {}".format(round(color_factor.r*10), round(color_factor.g*10), round(color_factor.b*10), round(time.time()-background.start_time)))
        #Timer added
        case 4:
            DrawText("R:{} G:{} B:{}                   Timer: {}".format(round(color_factor.r*10), round(color_factor.g*10), round(color_factor.b*10), round(background.check_timer())))
        #Only 50 moves and timer
        case 5:
            DrawText("R:{} G:{} B:{}   Moves Left: {}  Timer: {}".format(round(color_factor.r*10), round(color_factor.g*10), round(color_factor.b*10), round(background.check_moves()), round(background.check_timer())))
        case _:
            DrawText(" Roll: {}°                    Pitch: {}°".format(round(myimu.Roll),round(myimu.Pitch)))
      
    DrawBoard()
    pygame.display.flip()


def DrawGLInstructions():

    DrawText("How to play 3D Color Match:                ")
    pygame.display.flip()
    time.sleep(4)

    for i in range (12):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #Reset transformations
        glLoadIdentity() 
        gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
        #Depth perception
        glTranslatef(0.0,0.0, -5)   

        #Print RGB and other info on screen
        match i:
            #Given the answer key
            case 0:
                DrawText("Match the color of the front of the board...")
            case 1:
                DrawText("to the color of the background.            ")
            case 2:
                DrawText("Add or Remove Red, Green, and Blue...      ")
            case 3:
                DrawText("By tilting the controller                  ")
            case 4:
                DrawText("Add Red, Green, or Blue by tilting away... ")
            case 5:
                DrawText("Remove colors by tilting towards you.        ")
            case 6:
                DrawText("Tilt left to darken the color...            ")
            case 7:
                DrawText("Or tilt right to brighten the color.         ")
            case 8:
                DrawText("Your color values are on the bottom left... ")
            case 9:
                DrawText("They can range from 0 to 10!                ")
            case 10:
                DrawText("Let's get started!!                        ")
            case 11:
                DrawText("Try to match the answer key ------->       ")
            case _:
                DrawText("Red:{} Green:{} Blue:{}  {} {{{} {} {}}}".format(round(color_factor.r*10), round(color_factor.g*10), round(color_factor.b*10), color_factor.explainAction(), round(background.r*10), round(background.g*10), round(background.b*10)))
        
        DrawBoard()
        pygame.display.flip()
        time.sleep(4)


def SerialConnection():
    global serial_object
    serial_object = serial.Serial(port=myport.Name, baudrate=myport.Speed, timeout=myport.Timeout)
    print("Serial connection successful")

def extract_numbers(input_string):
    
    #Find Positive and Negative Integers
    match = re.findall(r"[-+]?\d*\.\d+|\d+", input_string)

    #If we found 2 matches
    if match:
        # Extract the numbers from the match groups
        number1 = float(match[0])
        number2 = float(match[1])

        return number1, number2
    else:
        # Return None if no match is found
        return None

def ReadData():
    while True:
        
        #Read serial line
        serial_input = serial_object.readline()
        #If length of the line is 9 bytes and the first byte is a $
        if serial_input[0] == 0x24: 
            
            result = extract_numbers(serial_input.decode('ascii'))

            if result:
                number1, number2 = result

                #Initialize start at 0 using roll and pitch errors
                if(myimu.roll_error == 0):
                    myimu.roll_error = number1
                if(myimu.pitch_error == 0):
                    myimu.pitch_error = number2
                
                myimu.Roll = number1 - myimu.roll_error
                myimu.Pitch = number2 - myimu.pitch_error
            else:
                print("No match found.")




def main():
    ConfWindw.mainloop()
    #If COM, speed, and difficulty were put in, start game
    if ApplicationGL == True:
        InitPygame()
        InitGL()

        try:
            #Check serial connection worked
            SerialConnection()
            #Check you can read data
            myThread1 = threading.Thread(target = ReadData)
            myThread1.daemon = True
            myThread1.start() 

            if(myport.Difficulty == 1):
                DrawGLInstructions()

            #Main loop
            while True:
                event = pygame.event.poll()
                #Check the exit button hasn't been pressed
                #if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                    break 
                
                #If not, update everything on the screen
                DrawGL()
                #If the background and the object match
                if (color_factor.compareBackground() or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    #Increase score
                    background.score+=1
                    #Print for timer difficulties
                    if(myport.Difficulty == 4):
                        #Adds the time form previous round to the timer
                        background.add_rollover_time()
                        DrawText("Score: {}             Rollover Time: {}".format(background.score, background.rollover_time))
                    else:   #Print for difficulties without timers
                        #Add the time rollover in the timer to the next round
                        DrawText("Score: {}".format(background.score))
                    pygame.display.flip()
                    time.sleep(4)
                    InitGL()
                #If out of moves, didn't win, and difficulty is 5
                #If the timer is 0 and difficulty is 4 or 5
                elif ((background.check_moves() == 0 and myport.Difficulty == 5)     or      (background.check_timer() == 0    and    (myport.Difficulty == 4 or myport.Difficulty == 5))):
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    DrawText("R:{} G:{} B:{}    {{{}  {}  {}}}   Final Score: {}".format(round(color_factor.r*10), round(color_factor.g*10), round(color_factor.b*10), round(background.r*10), round(background.g*10), round(background.b*10), background.score))
                    pygame.display.flip()
                    time.sleep(9)
                    RestartGL()
                    color_factor.reset_colors()
                pygame.time.wait(10)

        #If an error was caused
        except Exception as e:
            print(f"exception: {e}")
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            DrawText("Sorry, something is wrong :c")
            pygame.display.flip()
            time.sleep(5)

                 


if __name__ == '__main__': main()
'''
*** Momentary Switch - Polling with comparision to previous state of switch to prevent bounce and repeats
*** Good example to mimic the function of a TOGGLE SWITCH or a ROCKER SWITCH

*** This code does not use Interrupts, which is a better way to prevent bounce
*** I have used an internal LED PB

*** The code will "latch" one a push and then "unlatch" when pushed again

*** Connect a wire from 3.3V to the +ve common rail on the breadboard
*** Connect PB Switch to GP15 and the other to the +ve common rail
*** Connect PB LED to Pin GP13 and GND

*** See Fritzer sketch for wiring connections
'''

'''
*** load libraries both of which are common and come with Micropython. No need to download ***
'''
from machine import Pin   # it is possible to omit "import Pin". The code will then require "machine.Pin"
import utime

'''
*** Setup GPIO Constants ***
'''
GPIO_PB_LED = 13          # The Pushbutton's LED is connected to GPIO_13
GPIO_PB_SW = 15           # The Pushbutton's Switch contact is connected to GPIO_15
GPIO_BOARD_LED = 25       # The Pico's LED may be connected to GPIO_25

'''
*** Code Constants ***
'''
ON = True
OFF = False

'''
*** Setup LED OBJECTS ***
'''
try:
    On_Board_LED = Pin("LED", Pin.OUT)             # if "LED" is not recognised in this version it will report a TypeError
except TypeError:
    On_Board_LED = Pin(GPIO_BOARD_LED, Pin.OUT)    # so, we will use the old GPIO configuration to set the on board LED

PB_LED = Pin(GPIO_PB_LED, Pin.OUT)                 # Pushbutton LED
PB_Toggle = Pin(GPIO_PB_SW, Pin.IN, Pin.PULL_DOWN) # Push Button Switch

'''
*** Create variables: "Toggle Switch" and both LED's ***
'''
Toggle_State = OFF                                 # Toggle State
On_Board_LED.value(OFF)                            # Turn off On Board LDE
PB_LED.value(OFF)                                  # Turn off PB LED
PB_Toggle_Prev_State = PB_Toggle.value()           # Variable to hold Last PB State

'''
*** Main Program Function to check the state of the switch ***
'''
def Toggle_Btn_Handler():
    global PB_Toggle_Prev_State                    # getting variable and assigning global status
    global Toggle_State                            # using as global variable
    
    #utime.sleep_ms(1)  #If the switch has a lot of bounce- a dwell here can help
    
    if (PB_Toggle.value() == ON) and (PB_Toggle_Prev_State == OFF): #Pressed, If input is HIGH and different from before
        
        ''' Change state of Toggle variable by inverting current states '''
        PB_Toggle_Prev_State = not PB_Toggle_Prev_State
        Toggle_State = not Toggle_State
            
        On_Board_LED.value(Toggle_State)   # set Board LED status based on Toggle_State
        PB_LED.value(Toggle_State)         # set PB LED status based on Toggle_State
        print("Toggle State: Running code when Pushbutton is latched: " + str(Toggle_State))
        
    elif (PB_Toggle.value() == OFF) and (PB_Toggle_Prev_State == ON): #Released, If input is LOW and different from before
        
        ''' Invert Previous State '''
        PB_Toggle_Prev_State = not PB_Toggle_Prev_State
        
print("Ready, Steady, Go!")

'''
*** run an endless loop, unless Ctrl-C is pressed ***
'''
while True:
    
    try:
            
        Toggle_Btn_Handler()      # function to handle button presses            
        utime.sleep(.01)          #slow down the loop to mimic other processing activities
        
    except KeyboardInterrupt:     # code that handles Ctrl-C and when Stop is pressed
        
        print("Code Stopped. LED's reset.")
        PB_LED.value(OFF)         # turn off Pushbutton LED
        On_Board_LED.value(OFF)   # turn off On Board LED
        break                     # break the code and stop   
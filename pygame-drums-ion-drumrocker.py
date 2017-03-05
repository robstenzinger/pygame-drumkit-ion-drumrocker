import pygame

"""
pygame-drums-ion-drumrocker.py

This script is an experiment using PyGame make a Drum kit, to explore how to
turn the game-controller style drum kit into a set of electronic drums with
custom sounds.

Note and thanks: this project uses a pygame grew out of playing with
"joystick_calls.py" much of the example's structure remains:
http://programarcadegames.com/
http://simpson.edu/computer-science/

Also thanks: this script uses drum sounds from the awesome Sonic Pi project:
http://sonic-pi.net/

"""

#
# Define some colors
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


# sound mixer and channel
current_channel = 1
total_channels = 16
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.mixer.set_num_channels(total_channels)

# helper function to get the current usable sound channel
def get_channel():
    global current_channel
    if current_channel + 1 in range(1, total_channels):
        current_channel = current_channel + 1
    else:
        current_channel = 1

    return current_channel

# would be fun to prepare multiple sets of drums
drums = {}
drums["drumsset1"] = {}

# load sounds for drumset 1
drums["drumsset1"]["bass_hard"] = pygame.mixer.Sound("./sounds/drum_bass_hard.wav")
drums["drumsset1"]["bass_soft"] = pygame.mixer.Sound("./sounds/drum_bass_soft.wav")
drums["drumsset1"]["cowbell"] = pygame.mixer.Sound("./sounds/drum_cowbell.wav")
drums["drumsset1"]["ride_closed"] = pygame.mixer.Sound("./sounds/drum_cymbal_closed.wav")
drums["drumsset1"]["ride_hard"] = pygame.mixer.Sound("./sounds/drum_cymbal_hard.wav")
drums["drumsset1"]["ride_open"] = pygame.mixer.Sound("./sounds/drum_cymbal_open.wav")
drums["drumsset1"]["ride_pedal"] = pygame.mixer.Sound("./sounds/drum_cymbal_pedal.wav")
drums["drumsset1"]["ride_soft"] = pygame.mixer.Sound("./sounds/drum_cymbal_soft.wav")
drums["drumsset1"]["kick"] = pygame.mixer.Sound("./sounds/drum_heavy_kick.wav")
drums["drumsset1"]["snare_roll"] = pygame.mixer.Sound("./sounds/drum_roll.wav")
drums["drumsset1"]["snare_hard"] = pygame.mixer.Sound("./sounds/drum_snare_hard.wav")
drums["drumsset1"]["snare_soft"] = pygame.mixer.Sound("./sounds/drum_snare_soft.wav")
drums["drumsset1"]["splash_hard"] = pygame.mixer.Sound("./sounds/drum_splash_hard.wav")
drums["drumsset1"]["splash_soft"] = pygame.mixer.Sound("./sounds/drum_splash_soft.wav")
drums["drumsset1"]["tom_hi_hard"] = pygame.mixer.Sound("./sounds/drum_tom_hi_hard.wav")
drums["drumsset1"]["tom_hi_soft"] = pygame.mixer.Sound("./sounds/drum_tom_hi_soft.wav")
drums["drumsset1"]["tom_lo_hard"] = pygame.mixer.Sound("./sounds/drum_tom_lo_hard.wav")
drums["drumsset1"]["tom_lo_soft"] = pygame.mixer.Sound("./sounds/drum_tom_lo_soft.wav")
drums["drumsset1"]["tom_mid_hard"] = pygame.mixer.Sound("./sounds/drum_tom_mid_hard.wav")
drums["drumsset1"]["tom_mid_soft"] = pygame.mixer.Sound("./sounds/drum_tom_mid_soft.wav")


# default to 20 buttons, set them to cowbell to notice when a drum isn't yet mapped
buttons_map = ["cowbell"] * 20

# map the drum buttons to the drumset sounds
buttons_map[1] = "ride_closed"
buttons_map[2] = "ride_closed"
buttons_map[3] = "ride_closed"
buttons_map[4] = "ride_closed"
buttons_map[5] = "ride_closed"
buttons_map[6] = "ride_closed"
buttons_map[7] = "ride_closed"
buttons_map[8] = "kick"
buttons_map[11] = "tom_lo_soft"
buttons_map[12] = "snare_soft"
buttons_map[13] = "tom_mid_soft"
buttons_map[14] = "tom_hi_soft"
buttons_map[17] = "ride_pedal"
buttons_map[18] = "ride_open"
buttons_map[19] = "splash_soft"

# combos: the symbols on the ion drum rocker are actually button combos
combos = []
combo_map_to = []

# yellow symbol
combos.append([0,9,14])
# re-map this combo to a higher button
combo_map_to.append(17)

# blue symbol
combos.append([1,9,13])
# re-map this combo to a higher button
combo_map_to.append(18)

# green symbol
combos.append([9,11])
# re-map this combo to a higher button
combo_map_to.append(19)

# some buttons are not meant to trigger combos
not_combos = [2,3,4,5,6,7,8,10,12,15,16,17,20]

# the foot pedal is easy to get unintended hits because it's often held down
# ... at least that's a problem I have, I rest my foot on the pedal
hold_watch = [8]
hold_watch_down = []

# play the sound for the given button
def play_button_sound(button):
    global buttons_map
    if button in range(0, len(buttons_map)):
        if button not in hold_watch_down:
            soundChannel = pygame.mixer.Channel(get_channel())
            soundChannel.play(drums["drumsset1"][buttons_map[button]])
            if button in hold_watch:
                hold_watch_down.append(button)

# get the pygame party started...
pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pygame Drums")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    buttons = joystick.get_numbuttons()

    # first, capture the buttons being pressed
    compare_combo = []
    buttons_pressed = []
    for i in range(buttons):
        button = joystick.get_button(i)
        textPrint.print(screen, "button {:>2} value: {}".format(i,button))
        if i not in [6,7] and button > 0 and event.type == pygame.JOYBUTTONDOWN:
            print(i, ":", button)
            # play_button_sound(i)
            if i not in hold_watch_down:
                buttons_pressed.append(i)
        if i in hold_watch and event.type == pygame.JOYBUTTONUP:
            if i in hold_watch_down:
                hold_watch_down.remove(i)

    buttons_to_handle = len(buttons_pressed)

    # second, handle the list of buttons, whether:
    # ... individuals
    # ... combos
    # ... individuals + combos
    # ... combos + combos
    # ... etc...
    if len(buttons_pressed) == 1:
        # not a combo!
        print("buttons pressed: ")
        print(buttons_pressed)
        play_button_number = buttons_pressed[0]
        play_button_sound(play_button_number)
        buttons_to_handle -= 1
    else:
        # find combos and individuals
        # not a generic approach, using knowledge that the drum rocker only
        # has 3 combos (one for each symbol)
        play_combos = []
        combo0 = []
        combo1 = []
        combo2 = []
        for button_pressed in buttons_pressed:
            if button_pressed in not_combos:
                # not a combo
                play_button_sound(button_pressed)
                buttons_to_handle -= 1
            else:
                # which combo? assemble the buttons to find out...

                if button_pressed in combos[0]:
                    combo0.append(button_pressed)

                if button_pressed in combos[1]:
                    combo1.append(button_pressed)

                if button_pressed in combos[2]:
                    combo2.append(button_pressed)

        played_combo_buttons = []
        combo0played = False
        combo1played = False
        combo2played = False
        if len(combo0) == len(combos[0]):
            play_button_number = combo_map_to[0]
            play_button_sound(play_button_number)
            buttons_to_handle -= len(combo0)
            played_combo_buttons.extend(combo0)
            combo0played = True

        if len(combo1) == len(combos[1]):
            play_button_number = combo_map_to[1]
            play_button_sound(play_button_number)
            buttons_to_handle -= len(combo1)
            played_combo_buttons.extend(combo1)
            combo1played = True

        if len(combo2) == len(combos[2]):
            play_button_number = combo_map_to[2]
            play_button_sound(play_button_number)
            buttons_to_handle -= len(combo2)
            played_combo_buttons.extend(combo2)
            combo2played = True

        # some buttons used in combos aren't exclusive to combos...
        if len(combo0) > 0 and combo0played == False:
            if 14 in combo0:
                play_button_sound(14)
                buttons_to_handle -= 1

        if len(combo1) > 0 and combo1played == False:
            if 13 in combo1:
                play_button_sound(13)
                buttons_to_handle -= 1

        if len(combo2) > 0 and combo2played == False:
            if 11 in combo2:
                play_button_sound(11)
                buttons_to_handle -= 1

        #todo: were any unhandled buttons left over?
        if buttons_to_handle > 0:
            print("buttons_to_handle: {0}".format(buttons_to_handle))

    # update the screen
    pygame.display.flip()

    # tick the clock to keep the game moving forward
    clock.tick(100)

# closes the window when you quit
pygame.quit()

# Hacking Version 7
# This is a graphical password guessing game that displays a
# list of potential computer passwords. The player is allowed
# up to 4 attempts to guess the password. Each time the user
# guesses incorrectly, the number of correct letters in their
# correct locations is displayed and the user is prompted to
# make a new guess. The game indicates whether the player
# successfully guessed the password or not.

from uagame import Window
from time import sleep
from random import randint, choice

def main():
    location = [0,0]
    attempts = 4
    window = create_window()
    display_header(window, location, attempts)
    password = display_password_list(window, location)
    guess = get_guesses(window, password, location, attempts)
    end_game(window, guess, password)

def create_window():
    # Create a window for the game, open it and return it

    window = Window('Hacking', 600, 500)
    window.set_font_name('couriernew')
    window.set_font_size(18)
    window.set_font_color('green')
    window.set_bg_color('black')
    return window

def display_header(window, location, attempts):
    # Display the game header


    header = ['DEBUG MODE', str(attempts) + ' ATTEMPT(S) LEFT', '']
    for header_line in header:
        display_line(window, header_line, location)

def display_password_list(window, location):
    # Display the game passwords, update the location for the next
 

    embedded_size = 20
    password_list = ['PROVIDE', 'SETTING', 'CANTINA', 'CUTTING', 'HUNTERS', 'SURVIVE',  'HEARING', 'HUNTING', 'REALIZE', 'NOTHING', 'OVERLAP', 'FINDING', 'PUTTING']
    for password in password_list:
        # display embedded password
        password_line = embed_password(password, embedded_size)
        display_line(window, password_line, location)

    # display blank line
    display_line(window, '', location)

    # choose password
    return password_list[7]

def embed_password(password, size):
    # Return a fixed length string with the password embedded
  
    fill = '!@#$%^*()-+=~[]{}' # must not contain an ampersand
    password_size = len(password)
    embedding = ''
    split_index = randint(0, size - password_size)
    for index in range(0, split_index):
        embedding = embedding + choice(fill)
    embedding = embedding + password
    for index in range(split_index + password_size, size):
        embedding = embedding + choice(fill)
    return embedding

def get_guesses(window, password, location, attempts_left):
    # Input multiple guesses by the player and provide feedback.
   

    prompt = 'ENTER PASSWORD >'
    feedback_location = [window.get_width() // 2, 0]
    guess = prompt_user(window, prompt, location)
    attempts_left = attempts_left - 1

    while guess != password and attempts_left > 0:
        # get next guess
        window.draw_string(str(attempts_left), 0, window.get_font_height())
        check_warning(window, attempts_left)
        display_hint(window, password, guess, feedback_location)
        guess = prompt_user(window, prompt, location)
        attempts_left = attempts_left - 1
    return guess

def check_warning(window, attempts_left):
    # Check whether a lockout warning should be displayed and if so,
   
    warning_string = '*** LOCKOUT WARNING ***'
    if attempts_left == 1:
        # display warning
        warning_x = window.get_width() - window.get_string_width(warning_string)
        warning_y = window.get_height() - window.get_font_height()
        window.draw_string(warning_string, warning_x, warning_y)

def display_hint(window, password, guess, location):
    # Display the guess and the number of correct letters
   

    string = guess + ' INCORRECT'
    display_line(window, string, location)
    index = 0
    correct = 0
    max = len(password)
    for letter in guess:
        # check letter
        if (index < max) and (letter == password[index]):
            correct = correct + 1
        index = index + 1
    string = str(correct) + '/' + str(max) + ' IN MATCHING POSITIONS'
    display_line(window, string, location)

def end_game(window, guess, password):
 

    # clear window
    window.clear()

    # create outcome
    if guess == password:
        # create success
        outcome = [guess, '', 'EXITING DEBUG MODE', '', 'LOGIN SUCCESSFUL - WELCOME BACK', '']
        prompt = 'PRESS ENTER TO CONTINUE'
    else:
        # create failure
        outcome = [guess, '', 'LOGIN FAILURE - TERMINAL LOCKED', '','PLEASE CONTACT AN ADMINISTRATOR', '']
        prompt = 'PRESS ENTER TO EXIT'

    location = display_outcome(window, outcome)

    # prompt for end
    location[0] = (window.get_width() - window.get_string_width(prompt)) // 2
    prompt_user(window, prompt, location)

    # close window
    window.close()

def display_outcome(window, outcome):


    # compute y coordinate
    string_height = window.get_font_height()
    outcome_height = (len(outcome) + 1)*string_height
    y_space = window.get_height() - outcome_height
    line_y = y_space // 2

    location = [0, line_y]
    for outcome_line in outcome:
     #    compute x coordinate
        x_space = window.get_width() - window.get_string_width(outcome_line)

        location[0] = x_space // 2
        display_line(window, outcome_line, location)
    return location

def display_line(window, string, location):
  

    pause_time = 0.3
    window.draw_string(string, location[0], location[1])
    window.update()
    sleep(pause_time)
    location[1] = location[1] + window.get_font_height()
    
def prompt_user(window, prompt, location):
   

    input = window.input_string(prompt, location[0], location[1])
    location[1] = location[1] + window.get_font_height()
    return input

main()
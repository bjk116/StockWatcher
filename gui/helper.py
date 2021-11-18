"""
For helper gui functions
"""
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
import db
import data

def getxy(screen):
    return screen.getmaxyx()

def linebreak(screen):
    rows, cols = getxy(screen)

# The h stands for horizontal
def hcenter(screen, message, y=0):
    """
    Args:
        screen: curses screen object 
        message: str, what to display center horizontaly
    Returns:
        None, prints message in the middle of the cureses screen
    """
    num_rows, num_cols = getxy(screen)
    middle_row = int(num_rows / 2)
    # Calculate center column, and then adjust starting position based
    # on the length of the message
    half_length_of_message = int(len(message) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message

    # Draw the text
    print(str(screen), str(message), str(y))
    screen.addstr(y, x_position, message)

# The h stands for horizontal here as well
def hline(screen,size=10,y=0):
    hcenter(screen, "="*size, y=y)
    return y+1

def printColumns(screen, printvalues, size, y=0):
    """
    Args:
        screen: screen, ref to screen obj
        headers: list of string headers to print to screen
        size: int, how large should the headers take up
        y: int, first y coordinnate to start writing to
    Return:
        y: int, next safe y-coordinate to write to
    """
    column_width = int(size/len(printvalues))
    starting_x_position = [ x*column_width for x in range(0, len(printvalues))]
    for index, value in enumerate(printvalues):
        screen.addstr(y, starting_x_position[index], value)
    y+=1
    return y

def displayCurrentPrices(screen, size, y=0):
    """
    Args:
        screen: reference to screen object
        y: the starting y position for the text
    Returns:
        y, int, next safe y-coordinate to write to
    """
    currentPrices = data.getCurrentTickerValues()
    lastIndex = 0
    for index, (symbol, price, dt) in enumerate(currentPrices):
        printColumns(screen, [symbol, price, dt], size, y)
        lastIndex = index
    return lastIndex+y+1


def printHeaders(screen, headers, size, y=0):
    """
    Args:
        screen: screen, ref to screen obj
        headers: list of string headers to print to screen
        size: int, how large should the headers take up
        y: int, first y coordinnate to start writing to
    Return:
        y: int, next safe y-coordinate to write to
    """
    y = hline(screen, size=size,y=y)
    y = printColumns(screen, ["SYMBOL", "PRICE", "LAST RECIEVED"], size, y=y)
    y = hline(screen, size=size, y=y)
    y = displayCurrentPrices(screen, size, y=y)
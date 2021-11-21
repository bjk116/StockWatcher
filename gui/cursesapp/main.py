"""
The curses application because I like curses application.
"""
# TODO figure out the relative import required to get the db
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
import curses
import time
import helper

def startup():
    """
    Starts the screen and then changes how the keyboard inputs work
    to the curses standard.
    """
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    return screen

def endapplication(screen):
    """
    Undoes the keyboard changes made during startup.
    """
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

def displaySplash(screen):
    rows, cols = helper.getxy(screen)
    title = "Stock Watcher Alarm and Management System"
    helper.hcenter(screen, title)
    # Display a table
    # Top line
    helper.printHeaders(screen, ['SYMBOL', 'PRICE', 'TIME RECIEVED'], cols, y=cols)
    
    screen.refresh()

def initializeScreen():
    try:
        screen = startup() 
        displaySplash(screen)
        time.sleep(60)
    except Exception as e:
        # TODO setupt logging lol
        raise Exception(e)
    finally:
        endapplication(screen)

if __name__ == "__main__":
    initializeScreen()
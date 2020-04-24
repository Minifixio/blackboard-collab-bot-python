import sys
import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    return engine

def say(s):
    engine.say(s)
    engine.runAndWait()

# Using sys because of Threads issue
# Working on Mac, don't know on Windows
engine = init_engine()
say(str(sys.argv[1]))

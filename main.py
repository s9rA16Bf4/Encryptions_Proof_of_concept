#!/usr/bin/python
from PIL import Image
from random import randint
from os import system

"""

Encoding characters in plainsight by using different color schemes

"""

# Required
# PIL
# numpy

CTW = {}
ALPHA = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]
USED_COLOR_SCHEMES = []
LOGO = """
 ██▓███  ▓█████  █     █░    ██▓███  ▓█████  █     █░    ▄████▄   ▒█████   ▒█████   ██▓        ▄████▄   ▒█████   ██▓     ▒█████   ██▀███
▓██░  ██▒▓█   ▀ ▓█░ █ ░█░   ▓██░  ██▒▓█   ▀ ▓█░ █ ░█░   ▒██▀ ▀█  ▒██▒  ██▒▒██▒  ██▒▓██▒       ▒██▀ ▀█  ▒██▒  ██▒▓██▒    ▒██▒  ██▒▓██ ▒ ██▒
▓██░ ██▓▒▒███   ▒█░ █ ░█    ▓██░ ██▓▒▒███   ▒█░ █ ░█    ▒▓█    ▄ ▒██░  ██▒▒██░  ██▒▒██░       ▒▓█    ▄ ▒██░  ██▒▒██░    ▒██░  ██▒▓██ ░▄█ ▒
▒██▄█▓▒ ▒▒▓█  ▄ ░█░ █ ░█    ▒██▄█▓▒ ▒▒▓█  ▄ ░█░ █ ░█    ▒▓▓▄ ▄██▒▒██   ██░▒██   ██░▒██░       ▒▓▓▄ ▄██▒▒██   ██░▒██░    ▒██   ██░▒██▀▀█▄
▒██▒ ░  ░░▒████▒░░██▒██▓    ▒██▒ ░  ░░▒████▒░░██▒██▓    ▒ ▓███▀ ░░ ████▓▒░░ ████▓▒░░██████▒   ▒ ▓███▀ ░░ ████▓▒░░██████▒░ ████▓▒░░██▓ ▒██▒
▒▓▒░ ░  ░░░ ▒░ ░░ ▓░▒ ▒     ▒▓▒░ ░  ░░░ ▒░ ░░ ▓░▒ ▒     ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░   ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
░▒ ░      ░ ░  ░  ▒ ░ ░     ░▒ ░      ░ ░  ░  ▒ ░ ░       ░  ▒     ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░     ░  ▒     ░ ▒ ▒░ ░ ░ ▒  ░  ░ ▒ ▒░   ░▒ ░ ▒░
░░          ░     ░   ░     ░░          ░     ░   ░     ░        ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░      ░        ░ ░ ░ ▒    ░ ░   ░ ░ ░ ▒    ░░   ░
            ░  ░    ░                   ░  ░    ░       ░ ░          ░ ░      ░ ░      ░  ░   ░ ░          ░ ░      ░  ░    ░ ░     ░
"""

def generateColor():
        for n in ALPHA:
                color = (randint(0,255), randint(0,255), randint(0,255))
                while(color in USED_COLOR_SCHEMES is False):
                        color = (randint(0,255), randint(0,255), randint(0,255))
                CTW[n] = color

def readColorFromFile(image):
        im = Image.open(image)
        pix = im.load()
        width, height = im.size
        for x in range(width):
                for y in range(height):
                        if x in CTW.values() or y in CTW.values():
                                print("hi")

def encodeMessage(mess):
        ENCODED_MESSAGE = []
        for letter in mess:
                ENCODED_MESSAGE.append(CTW[letter])
        return ENCODED_MESSAGE

def decodeMessage(mess): # must be a list
        DECODED_MESSAGE = ""
        for color in list(mess):
                for value in CTW.keys():
                        if color == CTW[value]:
                            DECODED_MESSAGE += value
        return DECODED_MESSAGE

def writeToImage(ENCODED_MESSAGE, result):
        image = Image.new("RGB", (len(ENCODED_MESSAGE), len(ENCODED_MESSAGE)), color=None)
        pix = image.load()
        x = 0
        y = 0
        for n in ENCODED_MESSAGE:
           pix[x,y] = n
           x += 1
           if (x == len(ENCODED_MESSAGE)):
                y += 1
                x = 0

        image.save(result)
        print("¡ Image can be found in {}".format(result))

def main(image):
        run = True
        INPUT = None
        DECODED_MESSAGE = None
        VERSION = "1.0"
        ENCODED_MESSAGE = []
        generateColor() # Generates the colors for each char
        while(run):
                #system("clear") # Very linux special
                print("""
{0}
\tVersion {1}


input -> {2}
encoded -> {3}
decoded -> {4}

1) Take input
2) Encode image from input
3) Decode input from image
4) Write image
5) Quit
""".format(LOGO, VERSION, INPUT, ENCODED_MESSAGE, DECODED_MESSAGE)
)
                userInput = input(": ")
                if userInput == "1":
                        INPUT = input(">> ")
                elif userInput == "2":
                        if INPUT != None:
                               ENCODED_MESSAGE = [] # Reset
                               ENCODED_MESSAGE = encodeMessage(INPUT)
                elif userInput == "3":
                        DECODED_MESSAGE = decodeMessage(ENCODED_MESSAGE)
                elif userInput == "4":
                        writeToImage(ENCODED_MESSAGE, "result.png")
                elif userInput == "5":
                        run = False
                else:
                        print("Unknown argument {}".format(userInput))

if __name__ == "__main__":
        main("test.jpg")

#!/usr/bin/python
from PIL import Image
from random import randint, choice
from argparse import ArgumentParser
from os import system

CTW = {}
ALPHA = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ",
"1","2","3","4","5","6","7","8","9","0", "!", "@", "£", "#", "$", "¤", "%","€","&","/","{","[","(",")","]","=","}","+","?","`", "-", "_" ,"±", "A", "B", "C"
"D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "\n", "\t",".", ",", ";", ">", "<", "|"
, ":", '"']

def generateColor():
    USED_COLOR_SCHEMES = []
    for n in ALPHA: # For each letter
        color = (randint(1,255), randint(1,255), randint(1,255)) # generate a color
        while(color in USED_COLOR_SCHEMES is False): # if the color has already been picked
            color = (randint(0,255), randint(0,255), randint(0,255)) # generate a new one and try again
        CTW[n] = color # and finally we are done

def encodeMessage(mess):
        ENCODED_MESSAGE = []
        for letter in mess:
            try:
                if (len(letter) > 1):
                    for n in letter:
                        message = n
                        ENCODED_MESSAGE.append(CTW[message]) # appends the generated color code
                else:
                    message = letter
                    ENCODED_MESSAGE.append(CTW[message]) # appends the generated color code
            except KeyError:
                print("[!] Unknown character {}".format(message))
                exit()
        return ENCODED_MESSAGE

def decodeMessage(pathToFile, count):
    DECODED_MESSAGE = ""
    try:
        image = Image.open(pathToFile)
    except IOError:
        print("[!] Failed to open file {}".format(pathToFile))
        exit()

    x = 0
    y = 0
    width, height = image.size
    pixels = image.load()
    while(y != height):
        for value in CTW.keys():
            if (pixels[x,y] == CTW[value]): # have we found the key which returns the value of 'color'
                DECODED_MESSAGE += value # if thats the case then add the key to our string
        x += count
        if (x == width):
            x = 0
            y += 1

    return DECODED_MESSAGE

def writeToImage(ENCODED_MESSAGE, outputFileName, width, height, count, blanks):
    image = Image.new("RGB", (width, height), color=None) # Open the file
    pix = image.load() # Load it's contents to memory
    x = 0
    y = 0
    for n in ENCODED_MESSAGE:
        pix[x,y] = n # Adds the color code of n to the position of x and y in pix
        x += count
        if (x == width): # Have we reached the end of the line?
            y += count
            x = 0

    if (blanks): # We will fill all the black pixels with a random color
        x = 0
        y = 0
        while(x != width):
            if (pix[x,y] == (0,0,0)): # Is the color black?
                image.putpixel((x,y), choice(list(CTW.values()))) # Update it
            y += 1
            if (y == height):
                y = 0
                x += 1

    image.save(outputFileName) # Save the result
    print("[!] Image can be found in {}".format(outputFileName))

def storeEncoding(): # Used when saving the encoding to the computer
    openFile = open("enc.txt", "w")
    for n in CTW:
        code = CTW[n]
        if (n == "\n"): # Remove this and Satan will congratulate you
            n = "/n"
        elif (n == "\t"):
            n = "/t"
        openFile.write("{0}\t{1}\n".format(n, code))
    openFile.close()

def loadEncoding(file): # Loads the given encoding into memory
    openFile = open(file, "r")
    for n in openFile:
        char = n.split("\t")[0]
        code = n.split("\t")[1][1:-2] # Removes the \n at the end
        if (char == "/n"): # Remove this and Satan will congratulate you
            char = "\n"
        elif (char == "\t"):
            char = "/t"

        CTW[char] = eval(code) # Remove eval() and you will have hell
    openFile.close()

def updAlphabet(file):
    openFile = open(file, "r")
    for n in openFile:
        ALPHA.append(n[:-1])

def fastEncrypt(message, width, height, readFile, count, fillBlanks):
    generateColor()

    if (readFile): # We are gonna encrypt the contents of a file
        openFile = open(message, "r")
        message = []
        for n in openFile:
            message.append(n)

    ENCODED_MESSAGE = encodeMessage(message)
    writeToImage(ENCODED_MESSAGE, "result.png", width, height, count, fillBlanks)
    storeEncoding()

def fastDecrypt(imagePath, encPath, saveResult, runSys, count):
    loadEncoding(encPath)
    DECODED_MESSAGE = decodeMessage(imagePath, count)
    if (saveResult): # We need to save it to the harddrive
        openFile = open("decodedMessage.txt", "w")
        openFile.write(DECODED_MESSAGE)
        openFile.close()
        print("[!] The decoded message can be found in 'decodedMessage.txt'")
    elif (runSys):
        system(DECODED_MESSAGE)
    else:
        print("Decoded message: {}".format(DECODED_MESSAGE))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--store_enc", "-se", action="store_true", help="Saves the generated encot into the file enc.txt")
    parser.add_argument("--load_enc", "-le", help="Loads the given encoding into memory")
    parser.add_argument("--load_image", "-li", help="Loads an image into the program")
    parser.add_argument("--update_alpha", "-ua", help="Updates the internal alphabet with an additional amount of characters")
    parser.add_argument("--save_dec", "-sv", action="store_true", help="Saves the decrypted message to the harddrive, only usable with the --decrypt flag")
    parser.add_argument("--count", "-c", help="The distance between each pixel of data, usable when encrypting and decrypting")

    parser.add_argument("--fill_blanks", "-fb", action="store_true", help="Fills all the leftover pixels with garbage data")
    parser.add_argument("--sys", action="store_true", help="Tells the decrypter to run the decoded message, only usable with the --decrypt flag")
    parser.add_argument("--file", action="store_true", help="Marking that the contents of a file should be used to encrypt, only usable with the --encrypt flag")
    parser.add_argument("--width", help="Width of the generated picture")
    parser.add_argument("--height", help="Height of the generated picture")
    parser.add_argument("--encrypt", help="Encrypts the passed argument and saves it to the disk. The encoding used is automatically saved!")
    parser.add_argument("--decrypt", action="store_true", help="Decrypts the passed image and prints the result. (-le and -li are required)")

    args = parser.parse_args()
    store_enc = False
    file = None
    height = 10
    width = 10
    count = 1 # Default distance between each pod (pixel of data) is one
    fill_blank = False

    if (args.store_enc):
        store_enc = True
    if (args.fill_blanks):
        fill_blank = True
    if (args.load_image):
        file = args.load_image
    if (args.load_enc):
        loadEncoding(args.load_enc)
    if (args.update_alpha):
        updAlphabet(args.update_alpha)
    if (args.width):
        width = int(args.width)
    if (args.height):
        height = int(args.height)
    if (args.count):
        count = args.count

    if (args.encrypt):
        fastEncrypt(args.encrypt, width, height, args.file, int(count), fill_blank)
    elif (args.decrypt):
        if (args.load_image and args.load_enc):
            fastDecrypt(args.load_image, args.load_enc, args.save_dec, args.sys, int(count))
        else:
            print("main.py --decrypt -li <path/to/image> -le <path/to/enc> <optionalArgs>")
    else:
        parser.print_help()

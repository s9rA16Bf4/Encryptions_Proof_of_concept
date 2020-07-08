#!/usr/bin/env python
try:
    from PIL import Image
except ImportError:
    print("[!] You need to have Pillow (PIL) installed to be able to use this program")
    exit()
from random import randint, choice
from argparse import ArgumentParser
from os import system

CTW = {}
ALPHA = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ",
"1","2","3","4","5","6","7","8","9","0", "!", "@", "£", "#", "$", "¤", "%","€","&","/","{","[","(",")","]","=","}","+","?","`", "-", "_" ,"±", "A", "B", "C",
"D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "\n", "\t",".", ",", ";", ">", "<", "|"
, ":", '"']

def generateEncoding():
    USED_COLOR_SCHEMES = []
    for n in ALPHA: # For each letter
        color = (randint(1,255), randint(1,255), randint(1,255)) # generate a color
        while(color in USED_COLOR_SCHEMES is False): # if the color has already been picked
            color = (randint(0,255), randint(0,255), randint(0,255)) # generate a new one and try again
        CTW[n] = color # and finally we are done

def encryptMessage(mess):
        ENCODED_MESSAGE = []
        for value in mess:
            try:
                if (len(value) > 1): # its most likely the contents of file
                    for n in value: # so we need to break it down even more
                        localList = encryptMessage(n) # recursive call
                        for localX in localList: # Gather all the values
                            ENCODED_MESSAGE.append(localX) # and remember them
                else: # Its a single char
                    ENCODED_MESSAGE.append(CTW[value]) # appends the generated color code
            except KeyError:
                print("[!] Unknown character {}".format(value))

        return ENCODED_MESSAGE

def decryptMessage(pathToFile, count, width, height, encodingType):
    DECODED_MESSAGE = ""
    try:
        image = Image.open(pathToFile) # Try to open the picture
    except IOError:
        print("[!] Failed to open file {}".format(pathToFile))
        exit() # What's the point in continuing?

    if (width == None): # Get our canvas size
        width = image.size[0]
    if (height == None): # Get our canvas size
        height = image.size[1]

    y = 0

    if (encodingType == "ltr"):
        x = count
    elif (encodingType == "rtl"):
        x = width - 1
    elif (encodingType == "ttb" or encoding_type == "btt"):
        if (encoding_type == "btt"):
            y = height - 1
        x = 0

    pixels = image.load() # Get all the pixels
    if (encodingType == "ltr" or encodingType == "rtl"):
        while (y != height):
            for value in CTW.keys():
                if (pixels[x,y] == CTW[value]): # have we found the key which returns the value of 'color'
                    DECODED_MESSAGE += value # if thats the case then add the key to our string

            if (encodingType == "ltr"):
                x += count
                if (x >= width): # if we have reached the end of the x-axel then reset and jump one row down on the y-axel
                    x = count
                    y += count

            elif (encodingType == "rtl"):
                x -= count
                if (x < 0): # if we have reached the end of the x-axel then reset and jump one row down on the y-axel
                    x = width - 1
                    y += count
    elif (encodingType == "ttb" or encodingType == "btt"):
        while(x != width):
            for value in CTW.keys():
                if (pixels[x,y] == CTW[value]): # have we found the key which returns the value of 'color'
                    DECODED_MESSAGE += value # if thats the case then add the key to our string
            if (encodingType == "ttb"):
                y += count
                if (y >= height):
                    y = 0
                    x += count
            elif (encodingType == "btt"):
                y -= count
                if (y < 0):
                    y = height - 1
                    x += count

        if (y > height): # If we go out of bounds
            y = height # Just put us at the end

    return DECODED_MESSAGE

def saveImage(ENCODED_MESSAGE, outputFileName, width, height, count, blanks, updImage, encodingType):
    if (width == None and updImage == None):
        width = 10
    if (height == None and updImage == None):
        height = 10

    if (updImage != None): # We are gonna encrypt the message in the provided picture
        image = Image.open(updImage)
        width = image.size[0]
        height = image.size[1]
    else:
        image = Image.new("RGB", (width, height), color=None) # Open the file

    pix = image.load() # Load it's contents to memory
    if (encodingType == "ltr"):
        x = count
        y = 0
    elif (encodingType == "rtl"):
        x = width-1
        y = 0
    elif (encodingType == "ttb"):
        x = count
        y = 0
    elif (encodingType == "btt"):
        x = count
        y = height - 1

    for n in ENCODED_MESSAGE:
        pix[x,y] = n # Adds the color code of n to the position of x and y in pix
        if (encodingType == "ltr"):
            x += count
            if (x >= width): # Have we reached the end of the line?
                y += count
                if (y >= height):
                    print("[!] You must use a bigger canvas than height:{} width:{}".format(height, width))
                    exit()
                x = count
        elif (encodingType == "rtl"):
            x -= count
            if (x < 0): # Have we reached the end of the line?
                y += count # Jump one line down
                if (y >= height):
                    print("[!] You must use a bigger canvas than height:{} width:{}".format(height, width))
                    exit()
                x = width - 1
        elif (encodingType == "btt"):
            y -= count
            if (y < 0): # Have we reached the end of the line?
                x += count # Jump one line down
                if (y >= height):
                    print("[!] You must use a bigger canvas than height:{} width:{}".format(height, width))
                    exit()
                y = height - 1
        elif (encodingType == "ttb"):
            y += count
            if (y >= height): # Have we reached the end of the line?
                x += count # Jump one line down
                if (y >= height):
                    print("[!] You must use a bigger canvas than height:{} width:{}".format(height, width))
                    exit()
                y = 0

    if (blanks): # We will fill all the black pixels with a random color
        x = 0
        y = 0
        while(x != width):
            if (pix[x,y] == (0,0,0)): # Is the color black?
                image.putpixel((x,y), choice(list(CTW.values()))) # Update it with a random color
            y += 1
            if (y == height):
                y = 0
                x += 1

    image.save(outputFileName) # Save the result
    print("[!] Image can be found in {}".format(outputFileName))

def saveEncoding():
    openFile = open("enc.txt", "w")
    for n in CTW:
        code = CTW[n] # Remember it before we perhaps change the key, the value is the same
        if (n == "\n"): # Remove this and Satan will congratulate you
            n = "/n"
        elif (n == "\t"):
            n = "/t"
        openFile.write("{0}\t{1}\n".format(n, code)) # Write it down
    openFile.close()

def loadEncoding(file):
    openFile = open(file, "r")
    for n in openFile:
        char = n.split("\t")[0] # This grabs our character to use when identifying which color it will get
        code = n.split("\t")[1][1:-2] # Removes a couple of values, but this grabs the color code
        if (char == "/n"): # Remove this and Satan will congratulate you
            char = "\n"
        elif (char == "\t"):
            char = "/t"

        CTW[char] = eval(code) # Remove eval() and you will have hell
    openFile.close()

def updAlphabet(file):
    openFile = open(file, "r")
    for n in openFile:
        ALPHA.append(n[:-1]) # Removes the \n at the end of n and inserts it into the global alphabet list

def encrypt(message, width, height, readFile, count, fillBlanks, updImage, encodingType):
    if (len(CTW) == 0):
        generateEncoding() # Get the encoding
    if (readFile): # We are gonna encrypt the contents of a file
        openFile = open(message, "r")
        message = []
        for n in openFile:
            message.append(n)

    ENCODED_MESSAGE = encryptMessage(message) # Get the encrypted message
    saveImage(ENCODED_MESSAGE, "result.png", width, height, count, fillBlanks, updImage, encodingType) # Save it as an image
    saveEncoding() # Save the encoding used

def decrypt(imagePath, encPath, saveResult, runSys, count, width, height, encoding_type):
    loadEncoding(encPath)
    DECODED_MESSAGE = decryptMessage(imagePath, count, width, height, encoding_type)
    if (saveResult): # We need to save it to the harddrive
        openFile = open("decodedMessage.txt", "w")
        openFile.write(DECODED_MESSAGE)
        openFile.close()
        print("[!] The decoded message can be found in 'decodedMessage.txt'")
    elif (runSys):
        system(DECODED_MESSAGE)
    else:
        print("Decoded message: {}".format(DECODED_MESSAGE))

def genEncFromImage(pathToImage):
    try:
        image = Image.open(pathToImage)
    except IOError:
        print("[!] Failed to open the provided image {}".format(pathToImage))
        exit()
    pixels = list(image.getdata())
    USED_COLOR_SCHEMES = []
    for n in ALPHA: # For each letter
        found_pix = False # Used to identify if we have enough pixels
        for color in pixels:
            if ((color in USED_COLOR_SCHEMES) is False):
                CTW[n] = color # Assign the letter to the color
                USED_COLOR_SCHEMES.append(color)
                found_pix = True
                break
        if (found_pix != True):
            print("[!] Error: You need to have an image which consists of {} different colors/shades of pixels".format(len(ALPHA)))
            exit()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--encrypt", help="Encrypts the passed argument and saves it to the disk. The encoding used is automatically saved!")
    parser.add_argument("--decrypt", action="store_true", help="Decrypts the passed image and prints the result. (-le and -li are required)")
    parser.add_argument("--load_enc", "-le", help="Loads the given encoding into memory")
    parser.add_argument("--load_image", "-li", help="Loads an image into the program")
    parser.add_argument("--update_alpha", "-ua", help="Updates the internal alphabet with an additional amount of characters")
    parser.add_argument("--save_dec", "-sv", action="store_true", help="Saves the decrypted message to the harddrive, only usable with the --decrypt flag")
    parser.add_argument("--count", "-c", help="The distance between each pixel of data, usable when encrypting and decrypting")
    parser.add_argument("--fill_blanks", "-fb", action="store_true", help="Fills all the leftover pixels with garbage data")
    parser.add_argument("--sys", action="store_true", help="Tells the decrypter to run the decoded message, only usable with the --decrypt flag")
    parser.add_argument("--file", action="store_true", help="Marking that the contents of a file should be used to encrypt, only usable with the --encrypt flag")
    parser.add_argument("--width", help="Width of the generated picture, can also be used to get the x-side of where to look when decrypting")
    parser.add_argument("--height", help="Height of the generated picture, can also be used to get the y-side of where to look when decrypting")
    parser.add_argument("--gen_enc_from_image", "-gefi",help="Generates an encoding based of the pixels in the given image and saves it to the file 'enc.txt'")
    parser.add_argument("--include_in_pic", "-iip", help="Tells the encrypter that we shall use an image (provided by the user) instead of generating our own, only usable with the --encrypt flag")

    parser.add_argument("--right_to_left", "-rtl", action="store_true",help="Tells that you want the pixels to be placed right to left")
    parser.add_argument("--left_to_right", "-ltr", action="store_true", help="Tells that you want the pixels to be placed left to right (DEFAULT)")
    parser.add_argument("--top_to_bot", "-ttb", action="store_true", help="Tells that you want the pixels to be placed top to bot (you can use -ltr and -rtl here)")
    parser.add_argument("--bot_to_top", "-btt", action="store_true", help="Tells that you want the pixels to be placed bot to top (you can use -ltr and -rtl here)")



    args = parser.parse_args()
    file = None
    height = None
    width = None
    count = 1 # Default distance between each pod (pixel of data) is one
    fill_blank = False
    encoding_type = "ltr" # Default coding type is going from left to right

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
    if (args.gen_enc_from_image):
        genEncFromImage(args.gen_enc_from_image)
        saveEncoding()
        print("[!] Result can be found in the file 'enc.txt'")
        exit()
    if (args.right_to_left):
        encoding_type = "rtl"
    elif (args.bot_to_top):
        encoding_type = "btt"
    elif (args.top_to_bot):
        encoding_type = "ttb"

    if (args.encrypt):
        if (args.include_in_pic):
            encrypt(args.encrypt, width, height, args.file, int(count), fill_blank, args.include_in_pic, encoding_type)
        else:
            encrypt(args.encrypt, width, height, args.file, int(count), fill_blank, None, encoding_type)
    elif (args.decrypt):
        if (args.load_image and args.load_enc):
            decrypt(args.load_image, args.load_enc, args.save_dec, args.sys, int(count), width, height, encoding_type)
        else:
            print("main.py --decrypt -li <path/to/image> -le <path/to/enc> <optionalArgs>")
    else:
        parser.print_help()

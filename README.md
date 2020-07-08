# Color encryption
Encrypt messages in plainsight by combining letters with different colors of pixels!<br/>
It's now possible to use an image and encrypt a message into it!

## Where to begin?
Take a look at the Wiki to see some guidance on how the program works and how you can use it

## Installation
It's important that you have `Pillow` installed, the program will not work otherwise! Pillow can be installed through `pip` and or your package manager

## Example
![](https://github.com/s9rA16Bf4/colorEncryption/blob/master/pictures/1594210318_1411_08072020_1366x768.png)<p align=right>This is how "hello world" could look like. The structure is always the same but the generated pixels are random</p>

![](https://github.com/s9rA16Bf4/colorEncryption/blob/master/pictures/1594203312_1215_08072020_1366x768.png)
<p align=right>Same message as before, but this time all the other pixels also have a random color based upon the encryption table being used.</p>

![](https://github.com/s9rA16Bf4/colorEncryption/blob/master/pictures/1594210467_1414_08072020_1366x768.png)<p align=right>This image contains the word "hello" but with the pod (pixel of data) set to 4. This means that every part of the message is 4 pixels away from eachother</p>

![](https://github.com/s9rA16Bf4/colorEncryption/blob/master/pictures/1594209552_1359_08072020_1366x768.png)<p align=right>And this is the same message as before, the same pod but with the addition that the rest of the pixels consist of random colors</p>

![](https://github.com/s9rA16Bf4/colorEncryption/blob/master/pictures/1594210667_1417_08072020_1366x768.png)<p align=right>This image is pretty special, it contains the message "hello" and "world". But you can only find that out if you decrypt it with the pod set to 4 (this will get you "hello") and 3 ("world").  You of course need the correct encryption table to be able to decipher it</p>

## Challenges
1) http://q9j4vf8.atwebpages.com/

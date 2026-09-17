#Doppl-E | QR Code Generator
# Creates a QR code based off of a link, saves it as directed file name
# Used to create QR code for demo video
# Author : Jubal Clapp

import qrcode
qr = qrcode.make("https://github.com/jubalclapp/Doppl-E")
qr.save("dopple_qr.png")
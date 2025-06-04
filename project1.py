#QRcode generator program using qrcode library
#QRcode generator program using python

import qrcode
import image

qr = qrcode.QRCode(
    version=15, # version of QR code
    box_size=10, # size of each box in pixels
    border=5, # size of the border in boxes

)
data = "https://www.facebook.com/abid.mahamud.jim.2025" # data to be encoded in the QR code

qr.add_data(data) # add data to the QR code
qr.make(fit=True) # fit the QR code to the data
img = qr.make_image(fill_color="black", back_color="white") # create the QR code image

img.save("qrcode.png") # save the QR code image to a file
import myLib
import transfer

myLib.log("Welcome to SWT")

r = input("(S)end or (R)eceive ?: ")

if r.upper() == "S":
    transfer.send()
elif r.upper() == "R":
    transfer.receive()
else:
    myLib.log("Choose \"S\" or \"R\"")
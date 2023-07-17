import time
import binascii
import RPi.GPIO as GPIO   
from time import sleep

#initial setting
GPIO.setwarnings(False)    
GPIO.setmode(GPIO.BOARD)   
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.IN)

decoded = []
recval = []

def decode(recval):
        no_of_bits = len(recval) / 8
        no_of_bits_int = int(no_of_bits)
        no_of_bits = 8*no_of_bits_int
        recval = recval[0:no_of_bits]
        ul = 8
        ll = 0
        for i in range (0,no_of_bits_int):
            recvaltemp = recval[ll:ul]
            combined = "".join(str(x) for x in recvaltemp)
            combined = int(combined,2)
            converted = str(chr(combined))
            decoded.append(converted)
            ul = ul + 8
            ll = ll + 8
        try:
            decoded.remove("\x00")
        except:
            pass
        return decoded

def encode(text):
        biner = bin(int.from_bytes(text.encode(), 'big'))
        bin2list = biner[2:]
        listbin = []
        for i in bin2list:
            listbin.append(i)
        listbin.insert(0,"0")
        return listbin


text = "hi"#input("Input data to send: ")
print("Data to transmit: ",text)
encoded = encode(text)
print("\n\nTransmitting bits:" ,end=' ')
for i in range(len(encoded)):
    bit = encoded[i]
    print(bit,end=' ')
    if (bit == "0"):
        GPIO.output(12, GPIO.LOW)
    elif (bit == "1"):
        GPIO.output(12, GPIO.HIGH)
    time.sleep(0.5)
    recval.append(int(not GPIO.input( 11 )))
GPIO.output(12, GPIO.LOW) #clearing LED

recval = "".join(str(x) for x in recval)
print("\nReceived Bits:",recval)

decoded = decode(recval)
decoded = "".join(str(x) for x in decoded)
print("\nDecoded message:", decoded)

            


import serial
from Line_Tracking import *

line = Line_Tracking()
card = ""
all_cards=[]

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    try: 
        while True:
            if   line.IR01_GPIO.read() != True and line.IR02_GPIO.read() == True and line.IR03_GPIO.read() != True:
                print ('Middle')
            elif line.IR01_GPIO.read() != True and line.IR02_GPIO.read() != True and line.IR03_GPIO.read() == True:
                print ('Right')
            elif line.IR01_GPIO.read() == True and line.IR02_GPIO.read() != True and line.IR03_GPIO.read() != True:
                print ('Left')
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                try:
                    new_card = line.split(": ")[1]
                    if new_card != card:
                        card = new_card
                        if card not in all_cards:
                            all_cards.append(card)
                        print(card)
                except:
                    print("Not a card detected, probably.")

    except KeyboardInterrupt:
        line.IR01_GPIO.close()
        line.IR02_GPIO.close()
        line.IR03_GPIO.close()
        with open('all_cards.txt', 'w') as f:
            for card in all_cards:
                f.write(' '.join(card)+'\n')
        print ("\nEnd of program")


if __name__ == '__main__':
    main()
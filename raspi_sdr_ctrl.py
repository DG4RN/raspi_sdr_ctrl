#raspi_sdr_ctrl.py 
import board
import time
import busio
import RPi.GPIO as GPIO
import socket
import luma.core as luma
import adafruit_ads1x15.ads1115 as ADS

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from adafruit_ads1x15.analog_in import AnalogIn
from PIL import ImageFont, ImageDraw, Image
from gpiozero import CPUTemperature


 
 # Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C devices found:", [hex(device_address) for device_address in i2c.scan()])


# Address and Type of Display

device = ssd1306(port=1,address=0x3c, width=128, height=64)

# Schriftart laden

font = ImageFont.truetype('FreeSans.ttf', 12)
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((25, 25), "Start UP!", font=font, fill="white")
time.sleep(5)

i2c_1 = busio.I2C(board.SCL, board.SDA)
 # Create an ADS1115 object
ads = ADS.ADS1115(i2c_1)

 # Define the analog input channel
channel = AnalogIn(ads, ADS.P0) 

# GPIO Warning off
GPIO.setwarnings(False)
GPIO.cleanup()


# // Configure as Output Pin 18 (GPIO 24):
GPIO.setup(24, GPIO.OUT) # RX / TX Umschaltung

# // Configure as Output Pin 16 (GPIO 23):
GPIO.setup(23, GPIO.OUT) # LNA ON/ OFF

# // Configure as Output Pin 11 (GPIO 17):
GPIO.setup(17, GPIO.OUT) # ANT1 ON/ OFF

# // Configure as Output Pin 12 (GPIO 18):
GPIO.setup(18, GPIO.OUT) # ANT2 ON/ OFF

# // Configure as Output Pin 13 (GPIO 27):
GPIO.setup(27, GPIO.OUT) # ANT3 ON/ OFF

# Serveradresse und Port
host = '192.168.178.60'
port = 27299

# Server einrichten
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind ((host,port))
s.listen(1)

tx = False
lna = False
ant1 = False
ant2 = False
ant3 = False
message3 = 'Antenna ??'


while True:

 print('warten auf Verbindung...')
 conn, addr = s.accept()
 print('Verbindung von:', addr)


 data = conn.recv(1024)
 if not data:
        break
 print('Empfangene Daten:', data.decode('utf-8'))
 
 if data.startswith(b'TX'):
        print("Sender aktiviert")
        GPIO.output(24, GPIO.HIGH)  # Ausgang einschalten
        tx = True
        
              
 if data.startswith(b'RX'):
        print("Sender deaktiviert")
        GPIO.output(24, GPIO.LOW)  # Ausgang ausschalten
        tx = False
        
 if data.startswith(b'LNA1'):
        print("LNA aktiviert")
        GPIO.output(23, GPIO.HIGH)  # Ausgang einschalten
        lna = True
        
             
 if data.startswith(b'LNA0'):
        print("LNA deaktiviert")
        GPIO.output(23, GPIO.LOW)  # Ausgang ausschalten
        lna = False
        

 if data.startswith(b'ANT11'):
        print("Antenne 1 aktiviert")
        GPIO.output(17, GPIO.HIGH)  # Ausgang einschalten
        ant1 = True
        
              
 if data.startswith(b'ANT10'):
        print("Antenne 1 deaktiviert")
        GPIO.output(17, GPIO.LOW)  # Ausgang ausschalten
        ant1 = False
        

 if data.startswith(b'ANT21'):
        print("Antenne 2 aktiviert")
        GPIO.output(18, GPIO.HIGH)  # Ausgang einschalten
        ant2 = True
        
              
 if data.startswith(b'ANT20'):
        print("Antenne 2 deaktiviert")
        GPIO.output(18, GPIO.LOW)  # Ausgang ausschalten
        ant2 = False
        

 if data.startswith(b'ANT31'):
        print("Antenne 3 aktiviert")
        GPIO.output(27, GPIO.HIGH)  # Ausgang einschalten
        ant3 = True
        
              
 if data.startswith(b'ANT30'):
        print("Antenne 3 deaktiviert")
        GPIO.output(27, GPIO.LOW)  # Ausgang ausschalten
        ant3 = False
        
 
 cpu_temp = CPUTemperature()
 print(f"CPU Temperature: {cpu_temp.temperature} C")
 
 
 # Setup of Display content 
 if (tx): message1 = 'TX Aktiv'
 elif tx == False : message1 = 'RX mode'
 if (lna): message2 = 'LNA ON'
 elif lna == False : message2 = 'LNA OFF'
 if (ant1): message3 = 'Ant 1'
 if (ant2): message3 = 'Ant 2'
 if (ant3): message3 = 'Ant 3'

 message = f"{message1}\n {message2} {message3}\n Batt:{channel.voltage} V \n CPU Temp: {cpu_temp.temperature} C"
 with canvas(device) as draw:
              draw.text((5, 5), message, font=font, fill="white")

 
 print("Analog Value: ", channel.value, "Voltage", channel.voltage)
 time.sleep(1)
 
 #s.listen(1) 
  
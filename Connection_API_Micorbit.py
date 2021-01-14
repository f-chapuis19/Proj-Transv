import serial
import requests
import time

# send serial message
# Don't forget to establish the right serial port ******** ATTENTION
# SERIALPORT = "/dev/ttyUSB0"
SERIALPORT = "COM3"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():
    # ser = serial.Serial(SERIALPORT, BAUDRATE)
    ser.port = SERIALPORT
    ser.baudrate = BAUDRATE
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.timeout = None  # block read

    # ser.timeout = 0             #non-block read
    # ser.timeout = 2              #timeout block read
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    # ser.writeTimeout = 0     #timeout for write
    print("Starting Up Serial Monitor")
    try:
        ser.open()
    except serial.SerialException:
        print("Serial {} port not available".format(SERIALPORT))
        exit()

def sendUARTMessage(msg):
    ser.write(bytes(msg, 'utf-8'))
    print("Message <" + msg + "> sent to micro-controller." )

def getInProgressFire():
    request_fire = requests.get('http://146.59.150.159:10502/Simulateur-db/feux', timeout=5)
    if request_fire.status_code == 200:
        sendUARTMessage("reset")

        time.sleep(0.1)

        dict_fire = request_fire.json()
        for fire in dict_fire:
            sendUARTMessage(
                dict_fire[fire]['Localisation_X'] +
                "," + dict_fire[fire]['Localisation_Y'] + 
                "," + dict_fire[fire]['Intensite'])

            time.sleep(0.1)
    else:
        print('Error')

initUART()
while True:
    getInProgressFire()
    time.sleep(5)
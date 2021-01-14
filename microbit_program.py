from microbit import *

uart.init(baudrate = 115200)

while True:
    if uart.any():
        data = str(uart.read(), 'utf-8')
        if data == "reset":
            display.clear()
        else:
            data = data.split(",")
            x = int(data[0])
            y = int(data[1])
            intensity = int(data[2])
            if display.get_pixel(int(x // 2), int(y // 1.25)) < intensity:
                display.set_pixel(int(x // 2), int(y // 1.25), intensity)
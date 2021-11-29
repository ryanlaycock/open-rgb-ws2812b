import sacn
import time
import board
import neopixel
import os

num_of_leds = 300
pixels = neopixel.NeoPixel(board.D18, num_of_leds, auto_write=False)
print("Setup " + str(num_of_leds) + " LEDs on GPIO pin D18")

receiver = sacn.sACNreceiver()
receiver.start()  # start the receiving thread

print("Listening for DMX over E1.31 protocol on port 5568")

# define a callback function
@receiver.listen_on('universe', universe=1)  # listens on universe 1
def callback(packet):  # packet type: sacn.DataPacket
    setLights(packet, 0, 130)

@receiver.listen_on('universe', universe=2)  # listens on universe 1
def callback(packet):  # packet type: sacn.DataPacket
    setLights(packet, 131, 299)

def setLights(packet, start_n, end_n):
    led_n = start_n 
    packet_n = 0
    temp = []
    for v in packet.dmxData:
        # Check valid
        if v < 0 or v > 255:
            print("Invalid value recieved: " + str(v))
            return
        
        if led_n > end_n:
            pixels.show()
            return

        if packet_n != 0 and packet_n % 3 == 0:
            if len(temp) != 3:
                print("Incorrect RGB setting: " + str(temp))
                return

            # Set the LEDs RGB
            pixels[led_n] = temp
            temp = [] 
            led_n += 1 

        temp.append(v)
        packet_n += 1
    
    pixels.show()


# optional: if you want to use multicast use this function with the universe as parameter
receiver.join_multicast(0)

input("Press a key to stop...")

receiver.stop()

import UDP_Pico
import pico_blink

UDP_Pico.connect("0.0.0.0", 5005)

pico_blink.pico_blink(3)

while True:
    message = UDP_Pico.udp_receive(1024)
    #message_decoded = message.decoded
    print(message)

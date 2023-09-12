import UDP_pc
import time

message = "Hello World"
message_encoded = message.encode("utf-8")
user_IP_PORT = ("10.120.0.96", 5005)


while True:
    UDP_pc.UDP_send(message, user_IP_PORT)
    print(message)
    time.sleep(5)
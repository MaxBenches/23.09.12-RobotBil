from machine import Pin
import time

def define_gy53(gy53pin_number):
    gy53 = Pin(gy53pin_number, Pin.IN)
    return gy53

def getdistancegy53():
    define_gy53()
    while gy53.value() == True:
        pass
    while gy53.value() == False:
        pass
    starttime = time.ticks_us()
    while gy53.value() == True:
        pass
    endtime = time.ticks_us()
    microsec_diff = endtime - starttime
    millimeterdistance = microsec_diff / 10
    distance = millimeterdistance / 10
    print(f"Distance to surface: {distance} cm")
    return distance

while True:
    getdistancegy53()
    time.sleep(1)`
#!/usr/bin/env python
import time
import serial
import threading

def motor(motor1,motor2,motor3,motor4,motor5,motor6):
        global B
        B = [motor1,motor2,motor3,motor4,motor5,motor6]
        chare = cahre(B) + "D_"
        return chare
               
def cahre(dizi):
        string = ''
        for i in dizi:
                string = string + str(chr(i))
        return string

def degerult(deg1,deg2,deg3,deg4,deg5,deg6):
        global data
        global motor1, motor2, motor3, motor4, motor5, motor6
        motor1 = deg1
        motor2 = deg2
        motor3 = deg3
        motor4 = deg4
        motor5 = deg5
        motor6 = deg6
        data = motor(motor1,motor2,motor3,motor4,motor5,motor6)

#80 orta deger P
#40 alt deger F
#120 ust deger Z
# onsol, onsag, ortasol, ortasag, arkasol, arkasag
def paralel2():
        global durmasarti
        degerult(80,80,80,80,80,80)
        time.sleep(5)
        
        degerult(40,40,40,40,40,40)
        time.sleep(5)

        degerult(120,120,120,120,120,120)
        time.sleep(5)
        print("\n ---------- motorlar durdu ----------\n")
        durmasarti = False

def paralel1():
        global data
        global durmasarti
        while durmasarti:
                #ser.write(str(data).encode())
                time.sleep(0.010)

def paralel3():
        global datagelen
        #datagelen = ser.read(1)
        time.sleep(0.002)
        if(datagelen != ""):
                pass


def paralel4():
        global data
        global datagelen
        global durmasarti
        while durmasarti:
                print("giden veri " + data + " - gelen veri" + datagelen)
                time.sleep(1)

B = []
C = [None,None,None,None,None,None]
A = [80,80,80,80,80,80]
motor1 = 80
motor2 = 80
motor3 = 80
motor4 = 80
motor5 = 80
motor6 = 80
data = "PPPPPPD_"
datagelen = ""
durmasarti = True

if __name__ == '__main__':
        t1 = threading.Thread(target=paralel1)
        t2 = threading.Thread(target = paralel2)
        t3 = threading.Thread(target = paralel3)
        t4 = threading.Thread(target = paralel4)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t4.join()
        t3.join()
        t2.join()
        t1.join()
        print("durdu")
        time.sleep(60)

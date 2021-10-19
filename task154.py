import RPi.GPIO as GPIO

import matplotlib.pyplot as plt
import numpy as np

from time import sleep
import time

import string
import math

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)


D=[26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)


D1=[21, 20, 16, 12, 7, 8, 25, 24]


def decToBinList(decNumber):
    binary = bin(decNumber) [2:]
    binary = binary[::-1]
    l = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range (0, len(binary)):
        l[i] = int(binary[i])
        l.reverse()
        return l

def lightNumber(pins, List_num):
    for n in range (0, 8):
        GPIO.output(pins[n], 0)
    for j in range (7, -1, -1):
        GPIO.output(pins[j], List_num[j])
        
def num2dac(pins, K):
    L = decToBinList(K)
    lightNumber(pins, L)
    
def abc():
    a = 0
    b = 255
    i = int((a + b) / 2)
    while True:
        num2dac(D, i)
        num2dac(D1, i)
        time.sleep (0.01)
        if b - a == 2 or i == 0:
            Volt = int((int(i) * 3.3) / 256)
            print("Digital value: ", i, ", Analog value: ", Volt, "V")
            return i
            break
        elif GPIO.input(4) == 1:
            a = i
            i = int((a + b) / 2)
        elif GPIO.input(4) == 0:
            b = i
            i = int((a + b) / 2)
        
try:
    while abc() > 0:
        GPIO.output(17, 0)
        print('000')
        time.sleep(1)
        
    t_start = time.time()
    listT = []
    listV = []
    measure = []
    
    GPIO.output(17, 1)#зарядка конденсатора
    while abc() < 252:
        listT.append(time.time() - t_start)
        measure.append(abc())
        listV.append((abc() * 3.3) / 256)
        time.sleep(0.01)
        print(abc()*3.3 / 256)
        print("111")
        if abc() >= 252:
            break
    
    GPIO.output(17, 0)#зарядка конденсатора
    while abc() > 0:
        listT.append(time.time() - t_start)
        measure.append(abc())
        listV.append((abc() * 3.3) / 256)
        time.sleep(0.01)
        print("000")
        
    plt.plot(measure, 'r-')
    plt.show()
    
    np.savetxt('data.txt', measure, fmt='%f')
    
    dT = 0
    for i in range (0, len(listT)-1):
        dT = dT + abs(listV[i+1] - listV[i])
    dT = dT / (len(listT)-1)
    dV = 0
    for i in range (0, len(listT)-1):
        dV = dV + abs(listV[i+1] - listV[i])
    dV = dV / (len(listT)-1)
    x = [dT, dV]
    np.savetxt('setting.txt', x, fmt='%f')
    
    plt.plot(listT, listV, 'r-')
    plt.title('Зависимость напряжения от времени')# зависимость напряжения от времени
    plt.xlabe1('Время, с')# время
    plt.ylabe1('Навпряжение, В')# напряжение
    plt.show()

finally:
    for i in range (7, -1, -1):
        GPIO.output(pins[i], 0)
    
    
        
    
        
        


import threading
import sys
from scripts.base import BaseScript  # обязательный импорт для наследования
from ultralytics import YOLO
import cv2 as cv
import random
from time import sleep
from time import time
import dxcam
import win32api, win32con, win32gui
import math
from tools import telega
from threading import Thread
import socket
import pyautogui
import fLUXreborn
class ClassName(fLUXreborn.ClassName):
    def custom(self):
        sleep(2)
        for i in range(15):
            sleep(2.5)
            print(f"move f{100*i}")
            self.arduino.move(100*i, 0)
            sleep(0.7)
            print(f"move f{-100 * i}")
            self.arduino.move(-100*i, 0)
        sleep(4)
        for i in range(10):
            sleep(0.4)
            self.arduino.move(int(2*self.pi/10),0)
        sleep(2)
        self.mousemove(-2*self.pi,0)
        sleep(63)
        '''
        beta = 1500
        rads = 0
        alp = self.pi
        print(f"alp {alp}")
        t = 2
        turn = self.Turn(alp, beta, t)
        self.maketurn(turn)
        print(f"Your coords: {self.x, self.y, self.alp}\n")
        sleep(5)
        turn.mirror()
        sleep(1)
        self.maketurn(turn)
        print(f"Your coords: {self.x, self.y, self.alp}\n")
        sleep(33)
        '''
        #turn = self.Turn(0,0, 1.4,self.Dt(1.4))
        #self.maketurn(turn)
        while True:
            print(f"Your coords: {self.x,self.y,self.alp}\n")
            sleep(0.5)
            turn = self.decider()

            if turn is not None:
                self.movetoalp(turn.alp)
                self.movetoalp(turn.alp)
                self.movetoalp(turn.alp)
                self.maketurn(turn)
                self.mover.join()
                sleep(1)
                self.mousemove(-int(turn.beta / 2), 0)
                sleep(1)
                self.mousemove(int(turn.beta / 2), 0)
            sleep(4)
        alp =  int(10 * 360 / 1.103 * 90 / 60)
        alp = 13716
        print(alp)
        #alp = int(alp/4)
        beta = 2000
        sleep(2)
        print("asda")
        #self.hold_and_release_sleep('a',1.5)
        #self.mousemove(alp, 0)
        #sleep(0.1)
        #self.mousemove(alp, 0)
        #sleep(0.1)
        #self.mousemove(alp, 0)
        n = int(beta/100)
        xlast = beta-int(beta/100)*100

        sleep(2)

        while True:
            sleep(2)
            self.mover = Thread(target=self.hold_and_release_sleep, args=('s',2,))
            sleep(0.2)
            self.mover.start()
            sleep(0.6)
            self.mousemove(beta, 0, limiter=80)

            self.mover.join()
            sleep(0.5)
            self.mousemove(-int(beta/2),0)
            sleep(2)
            self.mousemove(int(beta / 2), 0)
            sleep(0.6)
            self.mousemove(int(alp/2)-beta, 0, limiter=325)
            sleep(0.6)




def run():
    script_class = ClassName()  # инициализация класса (сменить название на актуальное)
    script_class.custom()


if __name__ == "__main__":
    run()
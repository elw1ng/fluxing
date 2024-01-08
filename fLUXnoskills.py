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
import copy
import fLUXreborn
class ClassName(fLUXreborn.ClassName):  # Название класса (должен отличаться от других названий скриптов)

    def custom(self):
        sleep(1)
        if self.checker is None:
            self.checker = Thread(target=self.checkers, args=())
            self.checker.start()

        # self.camera.start(region=(8+self.rect[0], 31+self.rect[1], 640+self.rect[0]-8, 640+self.rect[1]-31), target_fps=self.target_fps)
        extrabarriertime = 0
        if self.ultrasave and self.ultrasavereturning:
            extrabarriertime = 8
        self.getNextFrame()

        ###
        Prediction = self.model.predict(source=self.img, device=0, conf=0.6, iou=0.2, imgsz=640, show=False,
                                        verbose=False)
        sleep(1)
        ###
        timer60power = time() - 60
        k = 0
        timer60 = time() - 60
        while (True):
            pererva = (time() - self.inittimer) / 2200
            if pererva - int(pererva) < 0.02 and pererva > 1:
                print("PERERVA")
                sleep(random.randint(90, 250))
            while self.reconnection:
                sleep(1)
                if time() - timer60 > 1200:
                    self.send_message_telega("Unable to coonect to server 20 mins")
                    sys.exit()
            # 10 pixels = 1.25degree
            self.lkmrelease()

            print(
                f"Spirit № {self.spiritCounter}  and {self.nospiritCounter} fails\n , working time: {(time() - self.inittimer) / 3600} hours , spirits per minute: {60 * self.spiritCounter / (time() - self.inittimer)}")

            self.getNextFrame()

            if not self.checker.is_alive() or self.ban or self.mainmenu or self.blackscreen:
                self.checker.join()
                if self.ban:
                    if self.mover is not None:
                        self.mover.join()
                    self.logout()
                elif not self.mainmenu:
                    self.send_message_telega("BANISHED BEFORE START")
                sys.exit()
            if self.stop:
                break
            started = False
            if self.SecretSpotSetting and self.justReturned:
                self.hold_and_release_sleep(self.moveback, 1.1)
                self.justReturned = False
            if time() - self.NoAnsweredThecalltime > self.StopifInactive:
                if k % 15 == 0:
                    self.send_message_telega("NO SPIRIT OCHEN DOLGO")
                k += 1
            while (not started):
                sleep(random.uniform(0.5, 1))
                if not self.checker.is_alive() or self.ban or self.mainmenu or self.blackscreen:
                    self.checker.join()
                    if self.ban:
                        if self.mover is not None:
                            self.mover.join()
                        self.logout()
                    elif not self.mainmenu:
                        self.send_message_telega("BANISHED BEFORE START")
                    sys.exit()
                if self.stop:
                    break
                if time() - self.NoAnsweredThecalltime > self.StopifInactive:
                    if k % 15 == 0:
                        self.send_message_telega("NO SPIRIT OCHEN DOLGO")
                    k += 1
                self.turn = None
                if self.turner is not None:
                    self.turner.join()
                while self.turn is None:
                    self.turn = self.decider()
                print(f"alp {self.turn.alp}")
                self.movetoalp(self.turn.alp)
                sleep(random.uniform(0.5, 1.2))
                self.fastselfcast(self.summon, 6.2, strafe=True)
                if self.mover is not None:
                    self.mover.join()
                sleep(0.3)
                if self.turner is None:
                    self.turner = Thread(target=self.maketurn, args=(self.turn,))
                    self.turner.start()
                else:
                    self.turner.join()
                    self.turner = Thread(target=self.maketurn, args=(self.turn,))
                    self.turner.start()
                startp = time()
                self.looptime = startp

                print("\n\nSTARTLOOP\n\n")

                started = self.startLoop()
                if self.restart:
                    self.restart = False
                    self.returning()
                    continue
                self.movetime = self.looptime - startp
            print("\n\nBALLLOOP\n\n")

            spiritdone = False
            firsttime = True
            while not spiritdone:
                self.looptime = time()
                if self.stop:
                    break

                self.strafe = True
                if self.mover is None:
                    self.mover = Thread(target=self.strafing, args=(True, 66, False, True,))
                    self.mover.start()
                else:
                    self.mover.join()
                    self.mover = Thread(target=self.strafing, args=(True, 66, False, True,))
                    self.mover.start()
                self.BallLoop(firsttime=firsttime, maxnoballtimer=1.7)
                self.strafe = False
                if self.mover is not None:
                    self.mover.join()
                max = 2
                extramove = random.randint(0, max)
                if extramove == max:
                    d = random.uniform(2.2, 4.8)
                    t = self.Td(d)
                    turn = self.Turn(self.alp - self.pi, 0, t, d)
                    self.movetoalp(turn.alp + self.pi)
                    sleep(random.uniform(0.12, 0.4))
                    if self.checkturn(turn):
                        self.maketurnw(turn)

                firsttime = False
                if self.restart:
                    self.restart = False
                    break

                checkrebuff = time() - timer60power > 60
                if checkrebuff:
                    while time() - timer60power < 60.04:
                        self.getNextFrame()

                        if not self.checker.is_alive() or self.ban or self.mainmenu or self.blackscreen:
                            self.checker.join()
                            if self.ban:
                                self.returning()
                                if self.mover is not None:
                                    self.mover.join()
                                self.logout()
                            elif not self.mainmenu:
                                self.send_message_telega("BANISHED before expel")
                            sys.exit()

                        if self.lowmana:
                            print("LOWMANA")
                            self.restart = True
                            self.gosave()
                        print("wait until 4 sec of expel")
                if checkrebuff:
                    # sleep(0.07)
                    timer60power = time()
                    self.fastselfcast(self.power, 4.6)

                else:
                    # sleep(0.07)
                    self.fastselfcast(self.power, 4.8)
                print("\n\nSPIRITLOOP\n\n")
                if self.stop:
                    break
                self.lkmrelease()
                spiritdone = self.SpiritLoop()
                self.lkmrelease()
            if self.restart:
                self.restart = False
                self.returning()
                break
            if self.stop:
                break

            self.returning()
            sl = random.randint(1, 20)
            if sl == 20:
                sleep(4)
                x = random.randint(-222, 222)
                y = random.randint(-666, 666)
                self.mousemove(x, y, limiter=random.randint(216, 511))
                sleep(11)
                self.mousemove(-x, -y, limiter=random.randint(216, 511))
                sleep(3)
            elif sl > 18:
                sleep(3.5)
                self.hold_and_release_sleep('space', 0.1)
                sleep(3.5)
            elif sl > 14:
                sleep(7.5)
            elif sl > 5:
                sleep(random.uniform(1.2, 3.5))
            else:
                sleep(0.8)

            '''
            for _ in range(320):
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 10, 0, 0, 0)
                sleep(0.02)
            sleep(10.1)
            '''

        self.camera.stop()
        print('Done.')
        pass


def run():
    script_class = ClassName()  # инициализация класса (сменить название на актуальное)
    script_class.custom()


if __name__ == "__main__":
    run()

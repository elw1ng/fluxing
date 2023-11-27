from scripts.base import BaseScript  # обязательный импорт для наследования
from ultralytics import YOLO
import cv2 as cv
import numpy as np
import os
import random
from time import sleep
from time import time
from PIL import Image, ImageGrab
import dxcam
import win32api, win32con, win32gui
import math
from tools import telega
from matplotlib import pyplot as plt
class ClassName(BaseScript):  # Название класса (должен отличаться от других названий скриптов)

    def __init__(self):
        super().__init__()  # инициализация класса после наследования

        """                   Ключи - Обязательное                   """

        self.name = "fluxing"  # имя в базе ключей
        self.keys = self.keys_data[self.name]  # загрузка настройки всех ключей данного скрипта
        self.keyActivate = self.keys["activate_key"]  # кнопка активации скрипта
        # обязательно скопировать ключ-значение "base", и переименовать согласно значению в self.name
        """ Полезное, но имеющее значение по дефолту, удалить при ненадобности """

        self.loop = True  # True активирует бесконечный цикл метода custom()
        self.debug = True  # Логи на стандартные функции

        """ Кастомные атрибуты писать здесь """
        self.debug = True
        self.mousereturn = [0, 0]
        self.model = YOLO("fishing.pt")  # load a pretrained YOLOv8n model
        #self.model = YOLO("bestOUTDOORnew.pt")  # load a pretrained YOLOv8n model

        # Get rect of Window
        self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        # hwnd = win32gui.FindWindow("UnrealWindow", None) # Fortnite
        self.rect = win32gui.GetWindowRect(self.hwnd)
        self.region = self.rect[0], self.rect[1], self.rect[2] - self.rect[0], self.rect[3] - self.rect[1]
        # initialize the WindowCapture class
        self.camera = dxcam.create()
        self.restart = False
        self.USER1_ID = self.keys['key17']['value']
        self.USER2_ID = self.keys['key18']['value']
        self.TOKEN = self.keys['key19']['value']
        self.target_fps = 59
        self.bot = telega.Telega(self.USER1_ID,self.USER2_ID, self.TOKEN)
        self.SleepMode=False
        self.stop = False
        self.lkmpressed = False

        self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        # hwnd = win32gui.FinwdWindow("UnrealWindow", None) # Fortnite
        self.rect = win32gui.GetWindowRect(self.hwnd)
        #region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
        print (self.rect[0],self.rect[1],self.rect[2],self.rect[3])

        self.img = None
        self.fpstimer= time()

    def getNextFrame(self):

        while time() - self.fpstimer < (1 / self.target_fps):
            sleep(0.001)
        img = self.camera.grab(
            region=(8 + self.rect[0], 31 + self.rect[1], 640 + self.rect[0] + 8, 640 + self.rect[1] + 31))
        while img is None:
            img = self.camera.grab(
                region=(8 + self.rect[0], 31 + self.rect[1], 640 + self.rect[0] + 8, 640 + self.rect[1] + 31))
        self.fpstimer = time()
        '''
        frameloop = time()
        img = self.camera.get_latest_frame()
        print(time()-frameloop)
        if time()-frameloop < 0.01:
            img = self.camera.get_latest_frame()
        '''
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

        self.img = img

    def _debug(self, text):
        if self.debug:
            print(f"DEBUG: {text}")

    # Посылает сообщение в телегу
    def send_message_telega(self, text):
        self.bot.send_message(f"{text} \n when {self.spiritCounter} spirits were fluxed and {self.nospiritCounter} summon fails,\n overall AFKtime = {self.AFKtime} seconds \n sultrasaves: {self.ultrasavecounter}")


    def lkmpress(self):
        if not self.lkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            self.lkmpressed = True
            return True
        return False

    def lkmrelease(self):
        if self.lkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        self.lkmpressed = False

    def spiritdetect(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[328:346, 290:350]
        if self.imgfind(img, self.SpiritFile, "mask.png"):
            self.NoAnsweredThecalltime = time()
            return True
        else:
            return False
    def checknospirit(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[358:372,223:244]
        if self.imgfind(img, "nospirit.png", "nospiritmask.png"):
            self.getNextFrame()
            if self.imgfind(img, "nospirit.png", "nospiritmask.png"):
                return True
            else:
                return False
        else:
            return False
    def checkdrawnspirit(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[358:372, 223:253]
        if self.imgfind(img, "drawnthespirit.png", "drawnthespiritmask.png"):
            self.getNextFrame()
            if self.imgfind(img, "drawnthespirit.png", "drawnthespiritmask.png"):
                return True
            else:
                return False
        else:
            return False
    def checklowmana(self , percentage = None , ignoresafemode = False ):
        result = True
        if not self.safeMode and not ignoresafemode:
            return False
        if percentage is None:
            percentage = self.lowmana_percentage
        # Read the images from the file
        bgrA=self.img[33:38, int(182 * percentage)]
        for i in range(5):
            bgr = bgrA[i]
            #print(bgr)
            if bgr[0]>=bgr[1]-1 and bgr[2]+1<bgr[0] and bgr[0]>4:
                result = False
        return result

    def imgfind(self, large_image, small_img, mask, conf=0.69 ):

        # Read the images from the file
        small_image = cv.imread(small_img)
        mask = cv.imread(mask)
        method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(large_image, small_image, method, None, mask)
        # We want the minimum squared difference
        _, mx, mxLoc, _ = cv.minMaxLoc(result)
        print(mx)
        if mx > conf and mx < 1.1:
            self.NoAnsweredThecalltime = time()
            return True
        else:
            return False

    def blackScreenDetect(self):

        # Read the images from the file

        img = self.img[0:66, 0:66]
        small_image = cv.imread("white.png")
       # cv.imshow("asdasd",small_image)


        small_image = small_image#[43:57, 60:88]
        large_image = img
        #cv.imshow("asdasd", large_image)
       # cv.waitKey(0)
        method = cv.TM_CCORR_NORMED
        result = cv.matchTemplate( large_image , small_image , method,None)
        # We want the minimum squared difference
        _, mx, _, _ = cv.minMaxLoc(result)
        if mx == 0:
            return True
        else:
            return False

    def custom(self):
        sleep(1)


        #self.camera.start(region=(8+self.rect[0], 31+self.rect[1], 640+self.rect[0]-8, 640+self.rect[1]-31), target_fps=self.target_fps)
        while True:
            self.getNextFrame()

                ###
            Prediction = self.model.predict(source="librak.mp4", device=0, conf=0.3, imgsz = 640 , show = True)
        sleep(1)
        ###

        self.camera.stop()
        print('Done.')
        pass


def run():
    script_class = ClassName()  # инициализация класса (сменить название на актуальное)
    script_class.custom()


if __name__ == "__main__":
    run()

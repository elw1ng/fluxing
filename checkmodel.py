from scripts.base import BaseScript  # обязательный импорт для наследования
from ultralytics import YOLO
import cv2 as cv
from time import sleep
from time import time
import dxcam
import win32gui
from tools import telega


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
        self.model = YOLO("bestNEW.pt")  # load a pretrained YOLOv8n model
        # self.model = YOLO("bestOUTDOORnew.pt")  # load a pretrained YOLOv8n model

        # Get rect of Window
        self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        # hwnd = win32gui.FindWindow("UnrealWindow", None) # Fortnite
        self.rect = win32gui.GetWindowRect(self.hwnd)
        self.region = self.rect[0], self.rect[1], self.rect[2] - self.rect[0], self.rect[3] - self.rect[1]
        # initialize the WindowCapture class
        self.camera = dxcam.create()
        self.restart = False
        self.selfcast = self.keys['key1']['value']
        self.moveback = self.keys['key2']['value']
        self.moveforward = self.keys['key3']['value']
        self.moveleft = self.keys['key4']['value']
        self.moveright = self.keys['key5']['value']
        self.power = self.keys['key6']['value']
        self.summon = self.keys['key7']['value']
        self.barrier = self.keys['key8']['value']
        self.kau = self.keys['key9']['value']
        self.feint = 'q'
        self.returnifNoAnswerTimer = int(self.keys['key10']['value'])  # seconds
        self.MoveForwardMultiplier = float(self.keys['key11']['value'])
        self.MaxMoveBackTimer = float(self.keys['key12']['value'])  # seconds
        self.StopifInactive = int(self.keys['key13']['value']) * 60  # 4 minutes
        self.MaxSpiritSize = int(self.keys['key14']['value'])  # in pixels
        self.SpiritFile = self.keys['key15']['value']
        self.Prefire = float(self.keys['key16']['value'])
        self.USER1_ID = self.keys['key17']['value']
        self.USER2_ID = self.keys['key18']['value']
        self.TOKEN = self.keys['key19']['value']
        self.target_fps = 45
        self.savemovetimer = 3
        self.savedelay = 100
        self.bot = telega.Telega(self.USER1_ID, self.USER2_ID, self.TOKEN)
        self.SleepMode = False
        self.NoAnsweredThecalltime = time()
        self.looptime = time()
        self.movetime = 0
        self.movecounter = 0
        self.stop = False
        self.lowmana_percentage = 0.07
        self.lkmpressed = False
        self.SuperSave = False
        self.lkmspam = True
        self.lkmballspam = False
        self.SecretSpotSetting = False
        self.justReturned = False
        self.safeMode = True

        self.spiritCounter = 0

        self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        # hwnd = win32gui.FinwdWindow("UnrealWindow", None) # Fortnite
        self.rect = win32gui.GetWindowRect(self.hwnd)
        # region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
        print(self.rect[0], self.rect[1], self.rect[2], self.rect[3])

        self.img = None
        self.fpstimer = time()

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


    def custom(self):

        # self.camera.start(region=(8+self.rect[0], 31+self.rect[1], 640+self.rect[0]-8, 640+self.rect[1]-31), target_fps=self.target_fps)
        while True:
            self.getNextFrame()

            ###
            Prediction = self.model.predict(source=self.img, device=0, conf=0.01, iou=0.2, imgsz=640, show=True)
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

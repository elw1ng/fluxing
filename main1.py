
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
from pyduino_mk.constants import *
from pyduino_mk import Arduino
import mss
import numpy as np

class ClassName(BaseScript):  # Название класса (должен отличаться от других названий скриптов)
    class Turn():
        def to_rad(self, alp):
            return (alp * math.pi / self.pi)

        def mirror(self):
            if self.alp >= self.pi:
                self.alp = self.alp - self.pi
            else:
                self.alp = self.alp + self.pi
            self.gamma = self.alp + int(self.beta / 2) - self.pi
            self.x = -self.x
            self.y = -self.y
        def generatetimings(self):
            n = random.randint(1, 2)
            dt = self.t / n
            for _ in range(n):
                tm = random.uniform(0.13, dt - 0.87)

                strtime = random.uniform(0.06, 0.14)
                tdel = random.uniform(0.1, dt - tm - 2 * strtime-0.2)
                str1 = ('a', tm, strtime)
                str2 = ('d', tdel, strtime)
                self.timings.append(str1)
                self.timings.append(str2)
        def __init__(self, alp, beta, t, avgd,strafes = False):
            self.pi = 6858
            self.alp = alp
            self.beta = beta
            self.t = t

            self.gamma = self.alp + int(self.beta / 2) - self.pi

            self.avgd = avgd
            self.x = self.avgd * math.sin(self.to_rad(self.gamma))
            self.y = self.avgd * math.cos(self.to_rad(self.gamma))
            self.limiter = random.randint(60, 100)
            self.strafes = strafes
            self.timings = []

            if self.strafes:
                self.generatetimings()





        def __eq__(self, other):
            return self.alp == other.alp and self.beta == other.beta and self.t == other.t




    def __init__(self):
        super().__init__()  # инициализация класса после наследования

        """                   Ключи - Обязательное                   """
        self.host_ip = "113.30.191.17"  # "188.72.203.58"
        self.port = 20035
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False

        print("Connecting to server")
        while not connected:
            # attempt to reconnect, otherwise sleep for 2 seconds
            try:
                self.client_socket.connect((self.host_ip, self.port))
                connected = True
                print("connection successful")
            except (ConnectionRefusedError):
                sleep(2)
                print("Unable to connect. try again")
        self.client_socket.settimeout(0.05)

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
        self.model = YOLO('best7nano100.pt')  # load a pretrained YOLOv8n model

        # self.model = YOLO("bestOUTDOORnew.pt")  # load a pretrained YOLOv8n model

        # Get rect of Window
        #self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        # hwnd = win32gui.FindWindow("UnrealWindow", None) # Fortnite
        #self.rect = win32gui.GetWindowRect(self.hwnd)
        #win32gui.SetForegroundWindow(self.hwnd)
        self.region = 1, 2, 3 - 4, 5 - 6
        # initialize the WindowCapture class
        #self.camera = dxcam.create()
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
        self.target_fps = 52
        if "fps" in sys.argv:
            self.target_fps = int(sys.argv[sys.argv.index("fps") + 1])
        self.bar = False
        if "bar" in sys.argv:
            self.bar = True
        self.savemovetimer = 2.5
        self.savedelay = 69
        self.bot = telega.Telega(self.USER1_ID, self.USER2_ID, self.TOKEN)
        self.SleepMode = True
        self.NoAnsweredThecalltime = time()
        self.looptime = time()
        self.movetime = 0
        self.movecounter = 0
        self.stop = False
        self.lowmana = False
        self.blackscreen = False
        self.lowmana_percentage = 0.07
        self.lkmpressed = False
        self.SuperSave = False
        self.lkmspam = True
        self.lkmballspam = False
        self.SecretSpotSetting = False
        self.justReturned = False
        self.safeMode = False
        self.nospiritRow = 0
        self.spiritCounter = 0
        self.nospiritCounter = 0
        self.AFKtime = 0
        self.lvling = False
        self.ultrasave = True
        self.ultrasavereturning = False
        self.ultrasavecounter = 0
        self.earlydamagesave = True

        #self.hwnd = win32gui.FindWindow(None, 'HDClone 6 Enterprise Edition ')
        # hwnd = win32gui.FinwdWindow("UnrealWindow", None) # Fortnite
        #self.rect = win32gui.GetWindowRect(self.hwnd)
        region = 1, 2, 3 - 4, 5 - 6
        #print(self.rect[0], self.rect[1], self.rect[2], self.rect[3])

        self.img = None
        self.fpstimer = time()

        self.t = None
        self.mover = None
        self.turner = None
        self.checker = None
        self.blackscreen_event = threading.Event()
        self.mainmenu = False
        self.ban = False
        self.mousemovetimer = time()
        self.camerastop = False
        self.c = Thread(target=self.videocamera, args=())
        self.c.start()
        self.reconnection = False
        sleep(1)
        self.inittimer = time()
        self.strafe = False
        # gps
        self.R = 14.0
        self.x = 0
        self.y = 0.01
        self.yelipse = 1.0
        self.overload = 0
        if "R" in sys.argv:
            self.R = float(sys.argv[sys.argv.index("R") + 1])
        if "e" in sys.argv:
            self.yelipse = float(sys.argv[sys.argv.index("e") + 1])
        self.alp = 0
        self.pi = 6858
        self.turns = []
        self.turn = None
        self.startextramove = False

    def movetoalp(self, alp):
        if alp >= 2 * self.pi:
            alp = alp - 2 * self.pi * int(alp / (2 * self.pi))
        if alp < 0:
            alp += 2 * self.pi
        d1 = alp - self.alp
        d2 = 2 * self.pi - d1
        if d1>=0:
            d2 = d1-2*self.pi
        else:
            d2 = 2*self.pi+d1
        deltas = []
        d = 0
        if abs(d1) < abs(d2):
            d = d1
        else:
            d = d2
        chance = 0.66
        while random.uniform(0.0, 1.0) <chance:
            delta = random.randint(-abs(int(d/5)),abs(int(d/5)))
            deltas.append(delta)
            d -= delta
            chance *= 0.6

        self.mousemove(d, 0,limiter = random.randint(255,510))
        for delta in deltas:
            sleep(random.uniform(0.05 , 0.12))
            self.mousemove(delta, 0, limiter=random.randint(255, 510))

        self.alp = alp

    def to_rad(self, alp):
        return (alp * math.pi / self.pi)

    def from_rad(self, rad):
        return int(rad * self.pi / math.pi)

    def Dt(self, t):
        if t >= 0.5:
            return 7.6 * t - 1.8
        else:
            return False

    def Td(self, d):
        if d >= 2:
            return (d + 1.8) / 7.6
        else:
            return False

    def generateturn(self):
        type = random.randint(1,4)
        if type <4:

            beta = random.randint(int(-self.pi/ 3.1 / type), int(self.pi/ 3.1 / type))
            rads = self.to_rad(beta)
            alp = self.fromcenteralp()
            d = 13.4
            print(f"alp {alp}")
            if rads == 0:
                t = 2.0
            else:
                mult = random.uniform(0.95, 1.03)
                t = self.Td(mult * 6.7 * rads / math.sin(rads / 2))
                d = d * mult
        else:
            beta = 0
            alp = self.fromcenteralp()
            d = 13.4
            print(f"alp {alp}")

            mult = random.uniform(0.95, 1.02)
            t = 2.14*mult
            d = d * mult
            return self.Turn(alp, beta, t, d,strafes=True)

        return self.Turn(alp, beta, t, d)

    def maketurn(self, turn):
        self.movetoalp(turn.alp)
        sleep(0.02)
        if self.mover is not None:
            self.mover.join()
            self.mover = Thread(target=self.hold_and_release_sleep, args=('s', turn.t,))

        else:
            self.mover = Thread(target=self.hold_and_release_sleep, args=('s', turn.t,))

        if not turn.strafes:
            self.mover.start()
            sleep(0.6)
            print("rotate")
            self.mousemove(turn.beta, 0, limiter=turn.limiter)
            print("end rotate")
            self.alp += turn.beta
            self.x += turn.x
            self.y += turn.y
            self.mover.join()
            sleep(random.uniform(0.09,0.18))
        else:
            self.mover.start()
            for strafe in turn.timings:
                k,dly,t = strafe
                sleep(dly)
                self.hold_and_release_sleep(k,t)
            self.x += turn.x
            self.y += turn.y
            self.mover.join()
            sleep(random.uniform(0.09, 0.18))


    def maketurnw(self, turn):
        self.movetoalp(turn.alp+self.pi)
        sleep(0.02)
        if self.mover is not None:
            self.mover.join()
            self.mover = Thread(target=self.hold_and_release_sleep, args=('w', turn.t,))
            self.mover.start()
        else:
            self.mover = Thread(target=self.hold_and_release_sleep, args=('w', turn.t,))
            self.mover.start()

        sleep(0.6)
        print("rotate")
        self.mousemove(turn.beta, 0, limiter=turn.limiter)
        print("end rotate")
        self.alp += turn.beta
        self.x += turn.x
        self.y += turn.y
        self.mover.join()
        sleep(random.uniform(0.3,1))

    def checkturn(self,turn):
        return math.pow(self.x + turn.x, 2) + math.pow(self.y + turn.y, 2) / math.pow(self.yelipse, 2) < math.pow(self.R - len(self.turns), 2)

    def decider(self):
        turn = self.generateturn()
        if math.pow(self.x + turn.x, 2) + math.pow(self.y + turn.y, 2) / math.pow(self.yelipse, 2) < math.pow(
                self.R - 0.5*len(self.turns)+0.1*self.overload, 2):
            #self.maketurn(turn)
            print(f"Turn with :{turn.alp, turn.beta, turn.t, turn.x, turn.y}")
            returning = copy.copy(turn)
            turn.mirror()
            self.turns.append(turn)
            self.overload = 0
            return returning

        else:
            self.overload += 1
            for turn in self.turns:
                if math.pow(self.x + turn.x, 2) + math.pow(self.y + turn.y, 2) / math.pow(self.yelipse, 2) < math.pow(
                        self.R, 2):
                    #self.maketurn(turn)
                    print(f"Turn from stack with  :{turn.alp, turn.beta, turn.t, turn.x, turn.y}")
                    returning = copy.copy(turn)
                    self.turns.remove(turn)
                    return returning

    def fromcenteralp(self):
        x = abs(self.x)
        y = abs(self.y)
        print(f"calculate center{self.x, self.y}")
        if y == 0:
            rad = math.pi / 2
        else:
            rad = math.atan(x / y)
        print(f"rad {rad}")
        if self.y < 0:
            rad += math.pi - rad

        if self.x < 0:
            rad = 2 * math.pi - rad
        print(f"real rad {rad}")
        alp = int(self.from_rad(rad))
        print(f"alp {alp}")
        return alp + random.randint(int(-self.pi / 2), int(self.pi / 2))

    def videocamera(self):
        while True:


            delta = time() - self.fpstimer

            fpstimer = 1 / self.target_fps

            if delta < fpstimer:
                sleep(fpstimer - delta)

            while self.camerastop:
                sleep(0.001)
            with mss.mss() as sct:
                img  = np.array(sct.grab((0,0, 30, 40)))

            while img is None:
                with mss.mss() as sct:
                    img = np.array(sct.grab((0, 0, 30, 40)))


            self.fpstimer = time()

            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

            self.img = img


    def getNextFrame(self, throttle=0.0):
        if self.t is not None:
            self.t.join()
            self.t = None
            self.camerastop = True
            sleep(1 / 20)
            self.camerastop = False
        while time() - self.fpstimer > 1 / 60:
            sleep(0.0005)
        '''
        while time() - self.fpstimer < (1 / self.target_fps):
            sleep(0.001)

        if throttle > 0:
            sleep(throttle)
        img = self.camera.grab(
            region=(8 + self.rect[0], 31 + self.rect[1], 640 + self.rect[0] + 8, 640 + self.rect[1] + 31))
        while img is None:
            img = self.camera.grab(
                region=(8 + self.rect[0], 31 + self.rect[1], 640 + self.rect[0] + 8, 640 + self.rect[1] + 31))
        self.fpstimer = time()
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        self.img = img
        '''

    def _debug(self, text):
        if self.debug:
            print(f"DEBUG: {text}")

    # Посылает сообщение в телегу
    def send_message_telega(self, text):
        try:
            self.bot.send_message(
                f"{text} \n when {self.spiritCounter} spirits were fluxed and {self.nospiritCounter} summon fails,\n overall AFKtime = {self.AFKtime} seconds  \n , working time: {(time() - self.inittimer) / 3600} hours , spirits per minute: {60 * self.spiritCounter / (time() - self.inittimer)}")
        except Exception:
            print("NO INTERNET CONNECTION... retry")
            sleep(30)
            self.send_message_telega(f"{text}")

    def checkDistanceY(self, box, img_h=640):
        x1, y1, x2, y2 = box.xyxy[0]
        c_y = ((y2 - y1) / 2) + y1

        return img_h / 2 - c_y

    def checkDistanceX(self, box, img_w=640):
        x1, y1, x2, y2 = box.xyxy[0]
        c_x = ((x2 - x1) / 2) + x1
        return img_w / 2 - c_x

    def checkDistance(self, box, img_w=640, img_h=640):
        x1, y1, x2, y2 = box.xyxy[0]
        c_x = ((x2 - x1) / 2) + x1
        c_y = ((y2 - y1) / 2) + y1
        return math.sqrt(math.pow(img_w / 2 - c_x, 2) + math.pow(img_h / 2 - c_y, 2))

    def mousemoveABS(self, x, y):
        pos = (x + 8 + self.rect[0], y + 31 + self.rect[1])
        win32api.SetCursorPos(pos)
        win32gui.SetForegroundWindow(self.hwnd)

    def pressLoc(self, mxLoc):
        win32gui.SetForegroundWindow(self.hwnd)
        self.mousemoveABS(mxLoc[0], mxLoc[1])
        self.lkmrelease()
        sleep(0.1)
        self.lkmpress()
        sleep(0.1)
        self.lkmrelease()
        sleep(0.1)

    def mousemove(self, x, y, timer=0.03, limiter=60,deltax=21,deltay=4):
        # limiter = 235
        nx = int(abs(x) / limiter)  # 35 UE5
        ny = int(abs(y) / limiter)
        if abs(x) > 0 or abs(y) > 0:
            if nx or ny  > 0:
                if x<0:
                    xstep = -limiter
                else:
                    xstep = limiter
                if y < 0:
                    ystep = -limiter
                else:
                    ystep = limiter
                xlast = x - xstep * nx
                ylast = y - ystep * ny
                lengthlast = abs(xlast)+abs(ylast)
                # timestep = timer / n
                timespent = 0

                kx = 0
                ky = 0
                for i in range(nx+ny):

                    decide = random.uniform(0.0,1.0)
                    chance = (nx-kx)/(nx+ny-kx-ky+1)
                    print(f"decide {decide} <? chance {chance} nx,kx {nx,kx}   ny ky {ny,ky}")
                    if ky == ny or decide < chance:
                        self.mousemovetimer = time()
                        self.arduino.move(xstep, 0)
                        kx += 1
                    else:
                        self.mousemovetimer = time()
                        self.arduino.move(0,ystep)
                        ky += 1


                    delay = time() - self.mousemovetimer
                    if (delay < timer):
                        sleep(timer - (delay))

                    # timespent+= time()-starttime
                # print(f"avgtimespentfor cycle = {timespent/n}")

                self.mousemovetimer = time()
                self.arduino.move(xlast, ylast)
                delay = time() - self.mousemovetimer
                lasttimer = timer * (lengthlast / limiter)
                if (delay < lasttimer):
                    sleep(lasttimer - (delay))

            else:
                self.mousemovetimer = time()
                self.arduino.move(x, y)
                delay = time() - self.mousemovetimer
                lasttimer = timer * ((abs(x)+abs(y)) / limiter)
                if (delay < lasttimer):
                    sleep(lasttimer - (delay))

    def MouseMove(self, box, img_w=640, img_h=640, scale=1, currentMousemove=None, limit=1200,changealp=False):
        # Check Closest

        at = 0
        centers = []

        x1, y1, x2, y2 = box.xyxy[0]
        if box.cls == 0 and (2 * (x2 - x1) < (y2 - y1)):
            y2 = y2 - random.uniform(0.1, 0.4) * ((y2 - y1) - (x2 - x1))
            # print("move upper")
        c_x = ((x2 - x1) / 2) + x1
        c_y = ((y2 - y1) / 2) + y1
        centers.append((c_x, c_y))
        dist = math.sqrt(math.pow(img_w / 2 - c_x, 2) + math.pow(img_h / 2 - c_y, 2))

        # Pixel difference between crosshair(center) and the closest object
        x = centers[at][0] - img_w / 2
        y = centers[at][1] - img_h / 2

        # Move mouse and shoot
        scalex = scale
        scaley = 1.0
        x = int(x * scalex)
        y = int(y * scaley)
        r1, r2 = self.get_angles([int(x + img_w / 2), int(y + img_h / 2)])
        #print(r1,r2)
        x = int(self.from_rad(r1))  # 2.8 UE 5
        y = int(self.from_rad(r2))
        if changealp:
            self.movetoalp(self.alp+x)
            x = 0
            sleep(0.03)
        #print(x,y)
        if x == 0 and y == 0:
            return False, currentMousemove

        if currentMousemove is not None and limit is not None:
            if math.sqrt(math.pow(currentMousemove[0] + x, 2) + 4 * math.pow(currentMousemove[1] + y, 2)) < 1.5 * limit:
                self.mousereturn[0] += x
                self.mousereturn[1] += y
                currentMousemove[0] += x
                currentMousemove[1] += y
                self.t = Thread(target=self.mousemove, args=(x, y))
                self.t.start()
                return True, currentMousemove
            else:
                return False, currentMousemove
        else:
            self.mousereturn[0] += x
            self.mousereturn[1] += y
            self.t = Thread(target=self.mousemove, args=(x, y))
            self.t.start()
            return True, None

    def confirmExisting(self, checkbox, precision=0.6, conf=0.05, i=3):

        newbox = None
        newbox_XDiff = None
        newbox_YDiff = None
        counter = 0
        for _ in range(i):
            found = False
            # sleep(1 / 60)
            self.getNextFrame()
            Prediction = self.model.predict(source=self.img, device=0, conf=conf, iou=0.3)
            detected_boxes = Prediction[0].boxes
            if len(detected_boxes) >= 1:
                for box in detected_boxes:
                    if (box.cls == checkbox.cls):
                        sizeDiff = abs(box.xyxy[0][2] - box.xyxy[0][0] - checkbox.xyxy[0][2] + checkbox.xyxy[0][0])
                        XDiff = abs(box.xyxy[0][0] - checkbox.xyxy[0][0])
                        YDiff = abs(box.xyxy[0][1] - checkbox.xyxy[0][1])
                        if sizeDiff < 30 and XDiff < 25 and YDiff < 25:
                            if not found:
                                newbox = box
                                newbox_XDiff = XDiff
                                newbox_YDiff = YDiff
                                found = True
                            else:
                                # dist1 = self.checkDistance(newbox)
                                # dist2 = self.checkDistance(box)
                                if XDiff * XDiff + YDiff * YDiff < newbox_XDiff * newbox_XDiff + newbox_YDiff * newbox_YDiff:
                                    newbox = box
                                    newbox_XDiff = XDiff
                                    newbox_YDiff = YDiff
                            if sizeDiff < 5 and XDiff < 8 and YDiff < 8:
                                checkbox = box
                                counter += 1
                                continue

            if found:
                checkbox = newbox
                counter += 1

        if float(counter) / i >= precision:
            return True, checkbox

        return False, None

    def track(self, checkbox, precision=0.6, conf=0.05, i=1):

        newbox = None
        newboxdist = None
        counter = 0
        for _ in range(i):
            found = False
            # sleep(1 / 60)
            self.getNextFrame()
            Prediction = self.model.predict(source=self.img, device=0, conf=conf, iou=0.3)
            detected_boxes = Prediction[0].boxes
            if len(detected_boxes) >= 1:
                for box in detected_boxes:
                    if (box.cls == checkbox.cls):
                        sizeDiff = abs(box.xyxy[0][2] - box.xyxy[0][0] - checkbox.xyxy[0][2] + checkbox.xyxy[0][0])
                        dist = self.checkDistance(box)
                        if sizeDiff < 30 and dist < 35:
                            if not found:
                                newbox = box
                                newboxdist = dist
                                found = True
                            else:
                                if dist < newboxdist:
                                    newbox = box
                                    newboxdist = dist
                            if newbox.conf > 0.4 and dist < 5:
                                return True, newbox

            if found:
                checkbox = newbox
                counter += 1

        if float(counter) / i >= precision:
            return True, checkbox

        return False, None

    def nextTarget(self, checkbox, conf=0.05):
        newbox = None
        counter = 0
        newbox_XDiff = None
        newbox_YDiff = None
        found = False
        # sleep(1 / 60)
        self.getNextFrame()
        Prediction = self.model.predict(source=self.img, device=0, conf=conf, iou=0.3)
        detected_boxes = Prediction[0].boxes
        if len(detected_boxes) >= 1:
            for box in detected_boxes:
                if (box.cls == checkbox.cls):
                    sizeDiff = abs(box.xyxy[0][2] - box.xyxy[0][0] - checkbox.xyxy[0][2] + checkbox.xyxy[0][0])
                    XDiff = abs(box.xyxy[0][0] - checkbox.xyxy[0][0])
                    YDiff = abs(box.xyxy[0][1] - checkbox.xyxy[0][1])
                    if sizeDiff < 45 and XDiff < 450 and YDiff < 450:
                        if not found:
                            newbox = box
                            newbox_XDiff = XDiff
                            newbox_YDiff = YDiff
                            found = True
                        else:
                            # dist1 = self.checkDistance(checkbox)
                            # dist2 = self.checkDistance(box)

                            if XDiff * XDiff + YDiff * YDiff >= 650 and \
                                    (
                                            newbox.conf < box.conf or newbox_XDiff * newbox_XDiff + newbox_YDiff * newbox_YDiff < 650):
                                newbox = box
                                newbox_XDiff = XDiff
                                newbox_YDiff = YDiff
                        if newbox.conf > 0.4 and newbox_XDiff * newbox_XDiff + newbox_YDiff * newbox_YDiff >= 650:
                            return True, newbox
        if found:
            return True, newbox
        return False, None

    def lkmpress(self):
        sleep(0.001)
        if not self.lkmpressed:
            self.arduino.press()
            self.lkmpressed = True
            return True
        return False

    def lkmrelease(self):
        sleep(0.001)
        if self.lkmpressed:
            self.arduino.release()
            self.lkmpressed = False
            return True
        return False

    def moveOnSpirit(self):
        self.getNextFrame()
        Prediction = self.model.predict(source=self.img, device=0, conf=0.2, iou=0.3)
        # print(Prediction[0].boxes.xyxy)

        detected_boxes = Prediction[0].boxes

        # debug the loop rate
        # print('FPS {}'.format(1 / (time() - loop_time)))
        # loop_time = time()
        print("i will check")
        if len(detected_boxes) >= 1:
            results = self.getBestBox(detected_boxes, 0)
            if not results is None:
                best_box = results[0]
                self.MouseMove(best_box)
                sleep(0.1)

    def BallLoop(self, firsttime=True, maxnoballtimer=2.6):
        if not firsttime:
            sleep(0.3)

        self.lkmrelease()
        self.lkmpress()
        ball_loop = True
        if firsttime:
            ball_was = False
        else:
            ball_was = True
        lkmpresstime = time()
        noballstime = time()
        noballstimeFull = noballstime
        kitetime = time()
        maxmousemove = [0, 0]
        while (ball_loop):
            if self.ban:
                self.fastselfcast(self.summon, 6.5)
                self.logout()
            if time() - noballstimeFull < 1:
                self.lkmrelease()
                self.lkmpress()
            '''
            if time() - kitetime > 10:
                sleep(0.1)
                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                self.mousereturn[0] = 0
                self.mousereturn[1] = 0
                self.hold_and_release_sleep(self.moveback, 1.5)
                kitetime = time()
                sleep(0.15)
                self.hold_and_release_sleep(self.moveforward, 1.5)
            '''
            if time() - self.looptime > 2.5 and not ball_was:
                print("noBALLSonspirit")
                self.restart = True
                self.gosave()
                return False

            '''
            if time() - self.looptime > 25:
                sleep(0.2)
                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                self.mousereturn[0] = 0
                self.mousereturn[1] = 0
                self.looptime = time()
                self.hold_and_release_sleep(self.moveforward, 1)
                sleep(1)
                self.movecounter += 1
            '''

            if (not ball_was):
                noballstime = time()
            if self.earlydamagesave and (
                    not ball_was or (ball_was and (time() - noballstimeFull < 1.1))) and self.lowmana:
                print("earlyLOWMANA")
                self.restart = True
                self.gosave()
                return False
            # sleep(1 / 60)
            self.getNextFrame()
            if self.blackscreen:
                self.blackscreen_event.wait()
                self.checker.join()
                if not self.ban and not self.mainmenu:
                    self.send_message_telega(f"BANISHED on {time() - noballstimeFull} sec in ballloop")
                sys.exit()

            Prediction = self.model.predict(source=self.img, device=0, conf=0.07)
            detected_boxes = Prediction[0].boxes

            if self.lowmana:
                print("LOWMANA")
                self.restart = True
                self.gosave()
                return False
            # debug the loop rate
            # print('FPS {}'.format(1 / (time() - loop_time)))
            # loop_time = time()

            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 1)
                if not results is None:

                    bestbox, _ = results

                    result = self.confirmExisting(bestbox, conf=0.05, i=1, precision=0.99)
                    confirmed = result[0]
                    bestbox = result[1]
                    scale = 1
                    # if confirmed:
                    holdtime = time()
                    if confirmed:
                        noballstime = time()
                        while time() - noballstime < 0.9:
                            if self.earlydamagesave and (
                                    not ball_was or (ball_was and (time() - noballstimeFull < 0.8))) and self.lowmana:
                                print("earlyLOWMANA")
                                self.restart = True
                                self.gosave()
                                return False
                            '''
                            if self.safeMode and (time() - noballstimeFull > 2):
                                if (time() - noballstimeFull > 6.5) and self.checklowmana(percentage=0.08):
                                    print("6.5 sec Timer + low mana in ballloop save")
                                    self.restart = True
                                    self.gosave()
                                    return False
                                elif (time() - noballstimeFull > 4) and self.checklowmana(percentage=0.09):
                                    print("4 sec Timer + low mana in ballloop save")
                                    self.restart = True
                                    self.gosave()
                                    return False
                                elif self.checklowmana(percentage=0.11):
                                    print("2 sec Timer + low mana in ballloop save")
                                    self.restart = True
                                    self.gosave()
                                    return False

                            if self.safeMode and self.checklowmana():
                                print("LOWMANA")
                                self.restart = True
                                self.gosave()
                                return False
                            '''
                            ml = self.checkDistance(bestbox)
                            if confirmed:
                                if ml < 10:
                                    scale = self.Prefire  # random.uniform(1, 1.2)
                                else:
                                    scale = 1 + (self.Prefire - 1) * ((100) / (ml * ml))
                                mouseresult = self.MouseMove(bestbox, scale=scale, currentMousemove=maxmousemove)
                                if mouseresult[0]:
                                    ball_was = True
                                    noballstime = time()
                                    if self.lkmpress():
                                        lkmpresstime = time()
                                    if self.lkmballspam:
                                        if time() - lkmpresstime > 0.21:
                                            self.lkmrelease()
                                            sleep(0.001)
                                            self.lkmpress()
                                            lkmpresstime = time()

                                else:
                                    break

                                maxmousemove = mouseresult[1]

                            if time() - holdtime < 0.70 and confirmed:
                                # sleep(0.02)
                                result = self.track(bestbox, conf=0.05, precision=0.99, i=1)
                                confirmed = result[0]
                                if confirmed:
                                    noballstime = time()
                                    bestbox = result[1]
                                else:
                                    result = self.nextTarget(bestbox, conf=0.05)
                                    confirmed = result[0]
                                    if confirmed:
                                        noballstime = time()
                                        bestbox = result[1]
                                        holdtime = time()
                            else:
                                # sleep(0.02)
                                result = self.nextTarget(bestbox, conf=0.05)
                                confirmed = result[0]
                                if confirmed:
                                    noballstime = time()
                                    bestbox = result[1]
                                    holdtime = time()

                    # print("Otpusk")
                    # if pressed:
                    #    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    #    pressed= False

            # if (ball_was) and (time() - noballstime > 1.0):
            # self.lkmrelease()
            # print("OTPUSK")
            if ball_was and (time() - noballstime > 0.3):
                self.strafe = False
            if (ball_was) and (time() - noballstime > 0.5) and (self.mousereturn[0] > 30 or self.mousereturn[1] > 30):
                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                self.mousereturn[0] = 0
                self.mousereturn[1] = 0
                maxmousemove = [0, 0]

            if (ball_was) and (time() - noballstime > maxnoballtimer) and (time() - noballstimeFull > 3.5):
                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                self.mousereturn[0] = 0
                self.mousereturn[1] = 0
                maxmousemove = [0, 0]
                ball_loop = False
                self.lkmrelease()
                print("ballstop")
            if (time() - noballstimeFull > 50):
                ball_loop = False
                self.lkmrelease()
            '''if self.safeMode and (time() - noballstimeFull > 2):
                if (time() - noballstimeFull > 6.5) and self.checklowmana(percentage=0.08):
                    print("6.5 sec Timer + low mana in ballloop save")
                    self.restart = True
                    self.gosave()
                    return False
                elif (time() - noballstimeFull > 4) and self.checklowmana(percentage=0.095):
                    print("4 sec Timer + low mana in ballloop save")
                    self.restart = True
                    self.gosave()
                    return False
                elif self.checklowmana(percentage=0.11):
                    print("2 sec Timer + low mana in ballloop save")
                    self.restart = True
                    self.gosave()
                    return False
            '''

    def getBestBox(self, detected_boxes, cls):

        best_box = None
        # bestboxdistFactor = None
        ballexist = False
        no_time = None
        for box in detected_boxes:
            if box.cls == cls:
                # distFactor = self.checkDistance(box)
                Y = self.checkDistanceY(box)
                # X = self.checkDistanceX(box)
                if -210 < Y < 210:
                    if not ballexist:

                        result = self.confirmExisting(box)

                        confirmed = result[0]
                        box = result[1]
                        if confirmed:
                            best_box = box
                            # bestboxdistFactor= distFactor
                            ballexist = True
                            no_time = time()
                    elif box.conf > best_box.conf and ballexist:
                        result = self.confirmExisting(box)

                        confirmed = result[0]
                        box = result[1]
                        if confirmed:
                            best_box = box
                            # bestboxdistFactor = distFactor
                            no_time = time()
        if ballexist:
            return best_box, no_time
        else:
            return None

    def lkmspamer(self):
        while self.lkmspam:
            sleep(0.215)
            self.lkmrelease()
            self.lkmpress()
        sleep(0.002)
        self.lkmrelease()

    def SpiritLoop(self, worktime=None):

        nodetectcounter =0
        starttime = time()
        spirit_loop = True
        nospirittime = starttime
        predictedtime = nospirittime
        extramove = False
        maxmousemove = [0, 0]
        detected = False
        while (spirit_loop):
            if worktime is not None and time() - starttime >= worktime:
                self.lkmrelease()
                return True

            self.getNextFrame()
            if self.lowmana:
                print("LOWMANA")
                self.restart = True
                self.gosave()
                return False
            if self.blackscreen:
                self.blackscreen_event.wait()
                self.checker.join()
                if not self.ban and not self.mainmenu:
                    self.send_message_telega(f"BANISHED in spiritloop")
                sys.exit()
            ###
            Prediction = self.model.predict(source=self.img, device=0, conf=0.15, iou=0.3)
            # print(Prediction[0].boxes.xyxy)

            detected_boxes = Prediction[0].boxes

            # debug the loop rate
            # print('FPS {}'.format(1 / (time() - loop_time)))
            # loop_time = time()
            # print("i will check")

            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 0)
                if not results is None:
                    predictedtime = time()
                    best_box = results[0]
                    result = self.MouseMove(best_box, currentMousemove=maxmousemove, limit=1450)
                    maxmousemove = result[1]
                    # sleep(0.05)
                    if self.spiritdetect():
                        self.lkmspam = True

                        #lkmspamer = Thread(target=self.lkmspamer, args=())
                        #lkmspamer.start()
                        nospirittime = time()
                        # print("click")
                        detected = True
                        self.lkmpress()

                        while self.spiritdetect():
                            if worktime is not None and time() - starttime >= worktime:
                                self.lkmspam = False
                                #lkmspamer.join()
                                self.lkmrelease()
                                return True

                            self.getNextFrame()
                            Prediction = self.model.predict(source=self.img, device=0, conf=0.15, iou=0.3)
                            # print(Prediction[0].boxes.xyxy)

                            detected_boxes = Prediction[0].boxes

                            # debug the loop rate
                            # print('FPS {}'.format(1 / (time() - loop_time)))
                            # loop_time = time()
                            # print("i will check")
                            if len(detected_boxes) >= 1:
                                results = self.getBestBox(detected_boxes, 1)
                                if not results is None:
                                    bestbox, _ = results
                                    result = self.confirmExisting(bestbox, conf=0.15, i=3, precision=0.99)
                                    confirmed = result[0]
                                    if confirmed:
                                        self.lkmspam = False
                                        self.lkmrelease()
                                        #lkmspamer.join()
                                        return False
                            if not extramove:
                                if len(detected_boxes) >= 1:
                                    results = self.getBestBox(detected_boxes, 0)
                                    if not results is None:
                                        bestbox, _ = results
                                        result = self.confirmExisting(bestbox, conf=0.15, i=1, precision=0.99)
                                        confirmed = result[0]
                                        if confirmed and (result[1].xyxy[0][2] - result[1].xyxy[0][0])<56 and  240<result[1].xyxy[0][0]<400:
                                            sleep(random.uniform(0.5,2.5))
                                            t= random.uniform(0.6,0.8)
                                            turn = self.Turn(self.alp-self.pi,0,t,self.Dt(t))
                                            self.maketurnw(turn)
                                            sleep(0.3)
                                            extramove = True
                            if self.blackscreen:
                                self.blackscreen_event.wait()
                                self.checker.join()
                                if not self.ban and not self.mainmenu:
                                    self.send_message_telega(f"BANISHED spiritloop")
                                sys.exit()
                            if self.lowmana:
                                print("LOWMANA")
                                self.restart = True
                                self.gosave()
                                self.lkmspam = False
                                self.lkmrelease()
                                return False
                        self.lkmspam = False

                        # print("release")
                        self.lkmrelease()

                        # result = self.confirmExisting(best_box, precision=0.3, conf=0.4)
                        # confirmed = result[0]
                        # if confirmed:
                        #     nospirittime = time()
                        # if (time() - holdtime > 26.0):
                        #     break;
            if time() - nospirittime > 14:
                spirit_loop = False
            if time() - nospirittime > 4.5 and not detected:
                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                self.mousereturn[0] = 0
                self.mousereturn[1] = 0
                nodetectcounter+=1
                if nodetectcounter ==10:
                    self.hold_and_release_sleep(' ',0.1)
                if nodetectcounter == 150:
                    self.movetoalp(self.alp - int(self.pi/3))
                    sleep(0.05)
                if nodetectcounter == 450:
                    self.movetoalp(self.alp + int(2*self.pi / 3))
                    sleep(0.05)


            if time() - predictedtime > 8 and detected:
                spirit_loop = False
            if time() - nospirittime > 7.5 and detected:
                spirit_loop = False

        self.spiritCounter += 1
        self.nospiritRow = 0
        return True

    def startLoop(self):

        start_loop = True
        startp = self.looptime
        nospirittime = time()
        released = False
        maxmousemove = [0, 0]
        status_confirmed = False
        while (start_loop):

            self.getNextFrame()
            if self.blackscreen:
                self.blackscreen_event.wait()
                self.checker.join()
                if not self.ban and not self.mainmenu:
                    self.send_message_telega(f"BANISHED on {time() - startp} sec in startloop")
                sys.exit()

            # print('FPS {}'.format(1 / (time() - loop_time)))
            # loop_time = time()

            while not status_confirmed:
                if (time() - self.looptime > 4.5):
                    self.nospiritCounter += 1
                    self.nospiritRow += 1
                    self.gosave()
                    return False
                if self.blackscreen:
                    self.blackscreen_event.wait()
                    self.checker.join()
                    if not self.ban and not self.mainmenu:
                        self.send_message_telega(f"BANISHED on {time() - startp} sec in startloop")
                    sys.exit()

                # if (time()-self.looptime > self.MaxMoveBackTimer) and not released:
                #     self.release(self.moveback)
                #     self.looptime = time()
                #     #sleep(0.4)
                #     print(f"{self.MaxMoveBackTimer} release")
                #     released = True
                if self.checkdrawnspirit():
                    print(f"spiritdrawned")
                    status_confirmed = True
                    if self.turner is not None:
                        self.turner.join()
                        self.turner = None
                        released = True
                    sleep(0.1)
                    self.movetoalp(self.alp - int(self.turn.beta / 3.5))
                    sleep(0.01)
                    break

                if not status_confirmed and self.checknospirit():
                    # sleep(0.3)
                    print(f"nospirit release")
                    self.nospiritCounter += 1
                    self.nospiritRow += 1
                    if self.turner is not None:
                        self.turner.join()
                        self.turner = None
                        released = True
                    sleep(0.2)
                    return False

                if self.lowmana:
                    print("LOWMANA")
                    self.restart = True
                    self.gosave()
                    return False

                self.getNextFrame()

            if self.turner is not None:
                self.turner.join()
                self.turner = None
                released = True

            self.getNextFrame()

            Prediction = self.model.predict(source=self.img, device=0, conf=0.2, iou=0.3)
            detected_boxes = Prediction[0].boxes

            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 0)
                if (not results is None):
                    best_box, nospirittime = results
                    result = self.confirmExisting(best_box, conf=0.2, precision=0.99, i=3)
                    confirmed = result[0]
                    best_box = result[1]

                    if confirmed and released:
                        # if not released:
                        #     self.release(self.moveback)
                        #     self.looptime = time()
                        #     #sleep(0.3)

                        self.lkmpress()
                        print("trying to move")
                        result = self.MouseMove(best_box, currentMousemove=maxmousemove, limit=1450,changealp = True)
                        maxmousemove = result[1]
                        # sleep(0.11)
                        if self.checkDistance(best_box) < 25:
                            if best_box.xyxy[0][2] - best_box.xyxy[0][0] < 40:

                                t = random.uniform(0.51, 0.61)
                                turn = self.Turn(self.alp - self.pi, 0, t, self.Dt(t))
                                if self.turner is None:
                                    self.turner = Thread(target=self.maketurnw, args=(turn,))
                                    self.turner.start()
                                else:
                                    self.turner.join()
                                    self.turner = Thread(target=self.maketurnw, args=(turn,))
                                    self.turner.start()

                                self.startextramove= True
                            return True
            '''
            if self.ultrasave and released and (time() - nospirittime > 5):
                self.lkmrelease()
                if self.ultrasavereturning:
                    self.gosave(nomessage=True, timer=2.5)
                    self.ultrasavecounter += 1
                    return True
                else:
                    self.restart = True
                    self.gosave(nomessage=True)
                    self.ultrasavecounter += 1
                    return False
            '''
            if (time() - nospirittime > 12):
                self.lkmrelease()
                self.restart = True
                self.gosave()
                return False
            if self.lowmana:
                print("LOWMANA")
                self.restart = True
                self.gosave()
                return False
        return True

    def get_angles(self, aim_target, window_size=[640, 640], fov=(60, 60)):
        fov = (math.radians(fov[0]), math.radians(fov[1]))

        x_pos = aim_target[0] / (window_size[0] - 1)
        y_pos = aim_target[1] / (window_size[1] - 1)

        x_angle = math.atan((x_pos - 0.5) * 2 * math.tan(fov[0] / 2))
        y_angle = math.atan((y_pos - 0.5) * 2 * math.tan(fov[1] / 2))

        phi = self.to_rad( self.mousereturn[1])
        if phi != 0:
            cosd = math.cos(phi) * math.cos(x_angle)
            d = math.acos(cosd)
            sinalp = math.sin(x_angle) / math.sin(d)
            alp = math.asin(sinalp)
            if phi > 0:
                y_angle += math.asin(math.cos(alp) * math.sin(d)) - phi
            else:
                y_angle += -math.asin(math.cos(alp) * math.sin(d)) - phi
            x_angle = math.atan(sinalp*math.tan(d))



        return ((x_angle), (y_angle))

    def fastselfcast(self, spell, casttime, strafe=False):
        if not self.checker.is_alive() or self.ban or self.mainmenu or self.blackscreen:
            self.checker.join()
            if self.ban:
                self.returning()
                if self.mover is not None:
                    self.mover.join()
                self.logout()
            elif not self.mainmenu:
                self.send_message_telega(f"VAS ZABANISHILI or VAS KICKNULO Vo vremya selfcasta knopki {spell}")
            sys.exit()
        # sleep(0.15)
        self.press(spell)
        # sleep(0.05)
        # self.hold_and_release_sleep(self.moveleft,0.1)
        self.press(self.feint)
        # sleep(0.05)
        # self.hold_and_release_sleep(self.moveright,0.1)
        self.press(self.selfcast)
        if strafe:
            self.strafe = True
            if self.mover is None:
                self.mover = Thread(target=self.strafing, args=(False, 27, True,))
                self.mover.start()
            else:
                self.mover.join()
                self.mover = Thread(target=self.strafing, args=(False, 27, True,))
                self.mover.start()
        sleep(casttime / 2)
        self.strafe = False
        sleep(casttime / 2)
        return True

    def spiritdetect(self):

        # Read the images from the file
        for i in range(3):
            self.getNextFrame()
            img = self.img[328:346, 290:350]
            if self.imgfind(img, self.SpiritFile, "mask.png"):
                self.NoAnsweredThecalltime = time()
                return True
        return False

    def checknospirit(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[348:382, 213:254]
        if self.imgfind(img, "nospirit.png", "nospiritmask.png", conf=0.91):
            self.getNextFrame()
            if self.imgfind(img, "nospirit.png", "nospiritmask.png", conf=0.91):
                return True
            else:
                return False
        else:
            return False

    def checkdrawnspirit(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[348:382, 213:263]
        if self.imgfind(img, "drawnthespirit.png", "drawnthespiritmask.png", conf=0.64):
            self.getNextFrame()
            if self.imgfind(img, "drawnthespirit.png", "drawnthespiritmask.png", conf=0.64):
                return True
            else:
                return False
        else:
            return False

    def checklowmana(self, percentage=None, ignoresafemode=False):
        result = True
        if not self.safeMode and not ignoresafemode:
            return False
        if percentage is None:
            percentage = self.lowmana_percentage
        # Read the images from the file
        bgrA = self.img[33:38, int(182 * percentage)]
        for i in range(5):
            bgr = bgrA[i]
            # print(bgr)
            if bgr[0] >= bgr[1] - 1 and bgr[2] + 1 < bgr[0] and bgr[0] > 4:
                result = False
        return result

    def checkGM(self, percentage=None, ignoresafemode=False):
        result = False

        # Read the images from the file
        bgrA = self.img[490:639, 1:150]
        for i in range(1, 149):
            rowcounter = 0
            for j in range(1, 149):
                bgr = bgrA[i][j]
                # print(bgr)
                sum = int(bgr[0]) + int(bgr[1])
                if bgr[2] > 70 and sum < int(bgr[2] / 2):
                    rowcounter += 1
            if rowcounter > 22:
                return True
        return result

    def gosave(self, nomessage=False, timer=None):
        self.restart = True
        if self.mover is not None:
            self.mover.join()
            self.mover = None
        if timer is None:
            delay = self.savedelay
        else:
            delay = timer
        self.AFKtime += delay
        print("TRYINGTOSTAYALIVE")
        if not self.SleepMode and not nomessage:
            self.send_message_telega("TRYING TO STAY ALIVe")
        self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
        self.mousereturn[0] = 0
        self.mousereturn[1] = 0
        for _ in range(1):
            self.getNextFrame()
            self.hold_and_release_sleep(self.moveback, self.savemovetimer)
        if self.SuperSave:
            sleep(0.05)
            self.press('4')
            sleep(0.05)
            self.hold_and_release_sleep(self.moveright, 0.5)
            # self.hold_and_release_sleep(self.moveleft,0.1)
            sleep(0.05)
            self.press(self.feint)
            sleep(0.05)
            self.hold_and_release_sleep(self.moveright, 0.5)
            # self.hold_and_release_sleep(self.moveright,0.1)
            sleep(0.05)
            self.press(self.selfcast)
            sleep(0.05)
            self.hold_and_release_sleep(self.moveleft, 1)
            self.hold_and_release_sleep(self.moveright, 1)
            self.hold_and_release_sleep(self.moveleft, 1)
            self.hold_and_release_sleep(self.moveright, 1)
            self.hold_and_release_sleep(self.moveleft, 1)
            self.press('5')
            self.hold_and_release_sleep(self.moveright, 1)
            self.press(self.feint)
            self.hold_and_release_sleep(self.moveleft, 1)
            self.press(self.selfcast)
            for _ in range(30):
                # if random.randint(1,10)>6:
                # self.press("SPACEBAR")
                self.hold_and_release_sleep(self.moveright, 1)
                self.hold_and_release_sleep(self.moveleft, 1)

            self.stop = True
            return False
        for _ in range(120):
            sleep(delay / 120)
            self.getNextFrame()

        for _ in range(1):
            self.hold_and_release_sleep(self.moveforward, self.savemovetimer * self.MoveForwardMultiplier)
            self.getNextFrame()

        self.justReturned = True
        return True

    def imgfind(self, large_image, small_img, mask, conf=0.69, loc=False):

        # Read the images from the file
        small_image = cv.imread(small_img)
        mask = cv.imread(mask)
        method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(large_image, small_image, method, None, mask=mask)
        # We want the minimum squared diff`erence
        _, mx, _, mxLoc = cv.minMaxLoc(result)
        if mx > conf and mx < 1.1:
            self.NoAnsweredThecalltime = time()
            if loc:
                return mxLoc
            return True
        else:
            if loc:
                return None
            return False

    def blackScreenDetect(self):

        # Read the images from the file

        img = self.img[20:70, 20:100]
        small_image = cv.imread("white.png")
        # cv.imshow("asdasd",small_image)

        small_image = small_image  # [43:57, 60:88]
        large_image = img
        # cv.imshow("asdasd", large_image)
        # cv.waitKey(0)
        method = cv.TM_CCORR_NORMED
        result = cv.matchTemplate(large_image, small_image, method, None)
        # We want the minimum squared difference
        _, mx, _, _ = cv.minMaxLoc(result)
        # print(mx)
        if mx == 0:
            return True
        else:
            return False

    def menuDetect(self):

        # Read the images from the file

        img = self.img[10:56, 10:113]
        if self.imgfind(img, "menu.png", "menumask.png", conf=0.6):
            self.mainmenu = True
            return True
        else:
            self.mainmenu = False
            return False

    def banDetect(self):

        # Read the images from the file
        img = self.img[460:490, 120:195]
        if self.imgfind(img, "ban.png", "banmask.png", conf=0.6):
            return True
        else:
            return False

    def returning(self):
        # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -mousereturn[0], -mousereturn[1], 0, 0)
        if self.t is not None:
            self.t.join()
            self.t = None
            sleep(1 / 35)
        print("ANGLES", self.mousereturn[0], self.mousereturn[1])
        self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
        self.mousereturn[0] = 0
        self.mousereturn[1] = 0

        sleep(0.05)
        max = 3
        extramove = random.randint(0,max)
        while extramove == max:
            d= random.uniform(2.8, 8.5)
            t = self.Td(d)
            turn = self.Turn(self.alp-self.pi+random.randint(int(-self.pi/6),int(self.pi/6)), random.randint(int(-self.pi/10),int(self.pi/10)), t, d)
            self.movetoalp(turn.alp+self.pi)
            sleep(random.uniform(0.5, 1.4))
            if self.checkturn(turn):
                self.maketurnw(turn)
            max += 2
            extramove = random.randint(0,max)


    def MoveBack(self):
        self.movecounter += 1
        self.hold_and_release_sleep(self.moveback, self.MaxMoveBackTimer)
        # sleep(0.75)

    def checkers(self):
        gmcheck = time()
        gmsent = False
        while True:
            sleep(1.2)
            try:
                command = self.client_socket.recv(1)
                command = command.decode()
                print(command)
                if command:
                    if int(command) >= 0:
                        self.send_message_telega("SAVING FROM BAN")
                        self.ban = True
                        break
                    else:
                        self.send_message_telega("SERVER ISSUE ")
                        self.ban = True
                else:
                    self.client_socket.close()

            except socket.timeout:
                pass
            except socket.error:
                # set connection status and recreate socket
                self.reconnection = True
                connected = False
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                print("connection lost... reconnecting")
                while not connected:
                    # attempt to reconnect, otherwise sleep for 2 seconds
                    try:
                        self.client_socket.connect((self.host_ip, self.port))
                        connected = True
                        print("re-connection successful")
                    except ConnectionRefusedError:
                        sleep(2)
                        print("Unable to connect. try again")
                self.client_socket.settimeout(0.05)
                self.reconnection = False

            if self.menuDetect():

                self.send_message_telega("MAIN MENU")

                for i in range(20):
                    sleep(0.5)
                    self.pressLoc((127, 360))
                    sleep(1)
                    self.getNextFrame()
                    if self.banDetect():
                        self.send_message_telega("BAN")
                        command = 0
                        command_with_time = f"{command}".encode()
                        self.client_socket.sendall(command_with_time)
                        break
                break
            if self.blackScreenDetect():
                self.blackscreen = True
                self.blackscreen_event.set()
                sleep(3)
                while self.blackScreenDetect():
                    sleep(1)
                    self.getNextFrame()
                    self.press(' ')
                sleep(2)
                if self.menuDetect():
                    self.send_message_telega("MAIN MENU")
                    for i in range(20):
                        sleep(0.5)
                        self.pressLoc((127, 360))
                        sleep(1)
                        self.getNextFrame()
                        if self.banDetect():
                            self.send_message_telega("BAN")
                            command = 0
                            command_with_time = f"{command}".encode()
                            self.client_socket.sendall(command_with_time)
                            break
                    self.blackscreen = False
                    self.blackscreen_event.clear()
                    break
                else:
                    self.blackscreen = False
                    self.blackscreen_event.clear()
                    break
            if self.checklowmana():
                print("LOWMANA")
                self.lowmana = True
            else:
                self.lowmana = False
            if self.checkGM():
                pass
            else:
                gmcheck = time()
            if time() - gmcheck > 14 and not gmsent and time() - self.fpstimer < 1:
                self.send_message_telega("GM!!!!!!!!!!!!!!!")
                gmsent = True

    def logout(self):
        print("log out")
        self.press(self.summon)
        # sleep(0.05)
        # self.hold_and_release_sleep(self.moveleft,0.1)
        self.press(self.feint)
        # sleep(0.05)
        # self.hold_and_release_sleep(self.moveright,0.1)
        self.press(self.selfcast)
        '''
        self.lkmrelease()
        pyautogui.press('esc')
        sleep(1)
        self.pressLoc((322,395))
        '''

    def strafing(self, jump=False, imax=11, mousemovement=False,morews = False):
        strafingtime = time()
        while self.strafe and time() - strafingtime < 5:
            strafetime = random.uniform(0.15, 0.58) * random.uniform(0.15, 0.58)
            i = random.randint(1, imax)
            if i == 1:
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('d', strafetime)
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('a', strafetime)
            elif i == 2:
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('d', strafetime)
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('a', strafetime)
            elif i == 3 or (morews and (i>=10 and i<=17)):
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('w', strafetime*1.4)
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('s', strafetime*1.4)
            elif i == 4 or (morews and (i>17 and i<=23)):
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('s', strafetime*1.4)
                sleep(random.uniform(0.2, 0.9) * random.uniform(0.2, 0.9))
                self.hold_and_release_sleep('w', strafetime*1.4)
            elif i == 5 and jump:
                sleep(0.2)
                self.hold_and_release_sleep(' ', 0.1)
                sleep(1.7)
            elif (i >= 6 and i <= 10) and mousemovement:
                x = random.randint(-1200, 1200)
                y = random.randint(-355, 355)
                self.mousemove(x, y)
                self.mousereturn[0] += x
                self.mousereturn[1] += y
                sleep(random.uniform(0.3 , 0.7))
                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]),limiter=random.randint(177,511))
                self.mousereturn[0] = 0
                self.mousereturn[1] = 0
            else:
                sleep(random.uniform(0.6, 0.9))
    def activatestrafe(self,i=61):
        self.strafe = True
        sleep(1)
        if self.mover is None:
            self.mover = Thread(target=self.strafing, args=(True, i, False, True,))
            self.mover.start()
        else:
            self.mover.join()
            self.mover = Thread(target=self.strafing, args=(True, i, False, True,))
            self.mover.start()


    def custom(self):
        sleep(1)

        if self.checker is None:
            self.checker = Thread(target=self.checkers, args=())
            self.checker.start()
        while True:
            for i in range(1111):
                sleep(0.001)
                print('movestart')
                self.arduino.move(55,0)
                print('moveend')
            for i in range(1111):
                sleep(0.001)
                print('movestart')
                self.arduino.move(-55,0)
                print('moveend')
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
            rebuffed = False
            pererva = (time() - self.inittimer) / 2200
            if pererva-int(pererva) < 0.02 and pererva > 1:
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
                sleep(random.uniform(0.5 , 1))
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
                sleep(random.uniform(0.5,1.2))
                if self.bar and (time() - timer60 > 47.5 - extrabarriertime):
                    if self.nospiritRow > 20:
                        sleep(90)
                        self.AFKtime += 90
                        continue
                    while (time() - timer60 < 60.05):
                        sleep(0.1)
                        self.getNextFrame()
                        if not self.checker.is_alive() or self.ban or self.mainmenu or self.blackscreen:
                            self.checker.join()
                            if self.ban:
                                if self.mover is not None:
                                    self.mover.join()
                                self.logout()
                            elif not self.mainmenu:
                                self.send_message_telega("BANISHED on trying to summon")
                            sys.exit()

                        if self.lowmana:
                            print("LOWMANA")
                            self.restart = True
                            self.gosave()
                    rebuffed = True
                    if self.lvling:
                        self.press(1)
                        sleep(13)
                    timer60 = time()
                    self.fastselfcast(self.barrier, 4)

                self.fastselfcast(self.summon, 6.2,strafe=True)
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

                thread = Thread(target=self.activatestrafe, args=(61,))
                thread.start()

                self.BallLoop(firsttime=firsttime, maxnoballtimer=1.7)
                thread.join()
                self.strafe = False
                if self.mover is not None:
                    self.mover.join()
                max = 4
                extramove = random.randint(0, max)
                if (self.turn.t > 2.2 or extramove) and not self.startextramove:
                    self.startextramove =False
                    d = random.uniform(2.2, 4.8)
                    t = self.Td(d)
                    turn = self.Turn(self.alp-self.pi, 0, t, d)
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

                elif not rebuffed:
                    # sleep(0.07)
                    self.fastselfcast(self.kau, 3.8)
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
            sl = random.randint(1,20)
            if sl ==20:
                sleep(4)
                x= random.randint(-222,222)
                y= random.randint(-666,666)
                self.mousemove(x,y,limiter=random.randint(216,511))
                sleep(11)
                self.mousemove(-x, -y, limiter=random.randint(216, 511))
                sleep(3)
            elif sl>18:
                sleep(3.5)
                self.hold_and_release_sleep('space',0.1)
                sleep(3.5)
            elif sl>14:
                sleep(7.5)
            elif sl>5:
                sleep(random.uniform(1.2,3.5))
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

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
import socket


# встановлюємо IP-адресу та порт хоста
host_ip = "192.168.0.177"
#host_ip = "193.33.38.56"
# замініть це на IP-адресу свого хоста
port = 12345

# підключаємося до хоста
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))
client_socket.settimeout(0.1)
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
        #self.model = YOLO("bestminusGamma.pt")  # load a pretrained YOLOv8n model
        self.model = YOLO("bestNEW.pt")  # load a pretrained YOLOv8n model

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
        self.returnifNoAnswerTimer = int(self.keys['key10']['value']) #seconds
        self.MoveForwardMultiplier = float(self.keys['key11']['value'])
        self.MaxMoveBackTimer = float(self.keys['key12']['value']) #seconds
        self.StopifInactive = int(self.keys['key13']['value'])*60 #4 minutes
        self.MaxSpiritSize = int(self.keys['key14']['value']) #in pixels
        self.SpiritFile = self.keys['key15']['value']
        self.Prefire = float(self.keys['key16']['value'])
        self.USER1_ID = self.keys['key17']['value']
        self.USER2_ID = self.keys['key18']['value']
        self.TOKEN = self.keys['key19']['value']
        self.target_fps = 45
        self.savemovetimer = 3
        self.savedelay = 100
        self.bot = telega.Telega(self.USER1_ID, self.USER2_ID, self.TOKEN)
        self.SleepMode=False
        self.NoAnsweredThecalltime = time()
        self.looptime = time()
        self.movetime = 0
        self.movecounter = 0
        self.stop = False
        self.lowmana_percentage = 0.02
        self.lkmpressed = False
        self.SuperSave = False

        self.SecretSpotSetting = False
        self.justReturned = False

        self.lkmspam = True
        self.lkmballspam = False

        self.rebuffCounter = 0
        self.spiritCounter = 0
        self.lastAntiAFKmove = 0
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
        self.bot.send_message(f"{text} \n when {self.spiritCounter} spirits were banished")

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
    def MouseMove(self, box, img_w=640, img_h=640, scale=1, currentMousemove = None, limit = 350):
        # Check Closest

        at = 0
        centers = []

        x1, y1, x2, y2 = box.xyxy[0]
        if box.cls == 2 and (2*(x2-x1) < (y2-y1)):
            y2 = y2 - random.uniform(0, 0.65)*((y2-y1)-(x2-x1))
            print("move upper")
        c_x = ((x2 - x1) / 2) + x1
        c_y = ((y2 - y1) / 2) + y1
        centers.append((c_x, c_y))
        dist = math.sqrt(math.pow(img_w / 2 - c_x, 2) + math.pow(img_h / 2 - c_y, 2))

        # Pixel difference between crosshair(center) and the closest object
        x = centers[at][0] - img_w / 2
        y = centers[at][1] - img_h / 2

        # Move mouse and shoot
        scalex = scale
        scaley = 0.9
        x = int(x * scalex)
        y = int(y * scaley)
        r1, r2 = self.get_angles([int(x + img_w / 2), int(y + img_h / 2)])

        x = int(10 * r1 / 1.125*90/75)
        y = int(10 * r2 / 1.125*90/75)

        if currentMousemove is not None and limit is not None:
            if math.sqrt(math.pow(currentMousemove[0]+x,2)+4*math.pow(currentMousemove[1]+y, 2)) < 2*limit:
                self.mousereturn[0] += x
                self.mousereturn[1] += y
                currentMousemove[0] += x
                currentMousemove[1] += y
                self.mousemove(x, y)
                return True, currentMousemove
            else:
                return False, currentMousemove
        else:
            self.mousereturn[0] += x
            self.mousereturn[1] += y
            self.mousemove(x, y)
            return True, None

    def confirmExisting(self, checkbox, precision=0.6, conf=0.01, i=3):

        newbox = None
        newbox_XDiff = None
        newbox_YDiff = None
        counter = 0
        for _ in range(i):
            found = False
            # sleep(1 / 60)
            self.getNextFrame()
            Prediction = self.model.predict(source=self.img, device=0, conf=conf, iou=0.2)
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

            if found:
                checkbox = newbox
                counter += 1

        if float(counter) / i >= precision:
            return True, checkbox

        return False, None
    def track(self, checkbox, precision=0.6, conf=0.03, i=1):

        newbox = None
        newboxdist = None
        counter = 0
        for _ in range(i):
            found = False
            # sleep(1 / 60)
            self.getNextFrame()
            Prediction = self.model.predict(source=self.img, device=0, conf=conf, iou=0.2)
            detected_boxes = Prediction[0].boxes
            if len(detected_boxes) >= 1:
                for box in detected_boxes:
                    if (box.cls == checkbox.cls):
                        sizeDiff = abs(box.xyxy[0][2] - box.xyxy[0][0] - checkbox.xyxy[0][2] + checkbox.xyxy[0][0])
                        dist = self.checkDistance(box)
                        if sizeDiff < 30 and dist < 25:
                            if not found:
                                newbox = box
                                newboxdist = dist
                                found = True
                            else:
                                if dist < newboxdist:
                                    newbox = box
                                    newboxdist = dist


            if found:
                checkbox = newbox
                counter += 1

        if float(counter) / i >= precision:
            return True, checkbox

        return False, None
    def nextTarget(self, checkbox, conf=0.03):
        newbox = None
        counter = 0
        newbox_XDiff = None
        newbox_YDiff = None
        found = False
        # sleep(1 / 60)
        self.getNextFrame()
        Prediction = self.model.predict(source=self.img, device=0, conf=conf, iou=0.2)
        detected_boxes = Prediction[0].boxes
        if len(detected_boxes) >= 1:
            for box in detected_boxes:
                if (box.cls == checkbox.cls):
                    sizeDiff = abs(box.xyxy[0][2] - box.xyxy[0][0] - checkbox.xyxy[0][2] + checkbox.xyxy[0][0])
                    XDiff = abs(box.xyxy[0][0] - checkbox.xyxy[0][0])
                    YDiff = abs(box.xyxy[0][1] - checkbox.xyxy[0][1])
                    if sizeDiff < 30 and XDiff < 120 and YDiff < 120:
                        if not found:
                            newbox = box
                            newbox_XDiff = XDiff
                            newbox_YDiff = YDiff
                            found = True
                        else:
                            # dist1 = self.checkDistance(checkbox)
                            # dist2 = self.checkDistance(box)

                            if XDiff * XDiff + YDiff * YDiff >= 400 and \
                                    (
                                            newbox.conf < box.conf or newbox_XDiff * newbox_XDiff + newbox_YDiff * newbox_YDiff < 400):
                                newbox = box
                                newbox_XDiff = XDiff
                                newbox_YDiff = YDiff
        if found:
            return self.confirmExisting(newbox, i=1)
        return False, None

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
    def BallLoop(self):
        ball_loop = True
        ball_was = False
        noballstime = time()
        noballstimeFull = noballstime
        kitetime = time()
        maxmousemove = [0, 0]
        while (ball_loop):

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
            if time() - self.looptime > 1 and not ball_was:
                self.lkmpress()
                sleep(0.35)
                self.lkmrelease()
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
            #sleep(1 / 60)
            self.getNextFrame()

            if self.blackScreenDetect():
                self.send_message_telega(f"{time() -noballstimeFull} sec,VAS ZABANISHILI or VAS KICKNULO vo vremya SHAROV")
                self.stop = True
                break

            Prediction = self.model.predict(source=self.img, device=0, conf=0.065)
            detected_boxes = Prediction[0].boxes

            if self.checklowmana():
                print("LOWMANA")
                self.restart = True
                self.gosave()
                return False
            # debug the loop rate
            # print('FPS {}'.format(1 / (time() - loop_time)))
            # loop_time = time()

            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 0)
                if not results is None:

                    bestbox, _ = results

                    result = self.confirmExisting(bestbox,conf=0.065,i=2,precision=0.99)
                    confirmed = result[0]
                    bestbox = result[1]
                    scale = 1
                    #if confirmed:
                    holdtime = time()
                    while confirmed:

                        if self.checklowmana():
                            print("LOWMANA")
                            self.restart = True
                            self.gosave()
                            return False
                        ml = self.checkDistance(bestbox)
                        if ml< 10:
                            scale = self.Prefire#random.uniform(1, 1.2)
                        else:
                            scale = 1+(self.Prefire-1)*((100)/(ml*ml))
                        mouseresult = self.MouseMove(bestbox, scale=scale,currentMousemove=maxmousemove)
                        noballstime = time()
                        if mouseresult[0]:
                            ball_was = True
                            noballstime = time()
                            if self.lkmpress():
                                lkmpresstime = time()
                            if self.lkmballspam:
                                if time() - lkmpresstime > 0.220:
                                    self.lkmrelease()
                                    sleep(0.001)
                                    self.lkmpress()
                                    lkmpresstime = time()

                        else:
                            break


                        maxmousemove = mouseresult[1]

                        if time() - holdtime < 0.255:
                            sleep(0.050)
                            result = self.track(bestbox, conf=0.065, precision=0.99, i=1)
                            confirmed = result[0]
                            bestbox = result[1]
                        else:
                            result = self.nextTarget(bestbox, conf=0.065)
                            confirmed = result[0]
                            bestbox = result[1]
                            holdtime = time()

                    #print("Otpusk")
                    #if pressed:
                    #    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    #    pressed= False
            try:
                command_with_time = client_socket.recv(1024)
                command = command_with_time.decode()

                # виконуємо команду та виводимо час її отримання
                print(f"Command '{command}' received")
                if int(command) > 0:
                    ball_loop = False
                    self.lkmrelease()
                    print("Otpusk po prikazu")
            except socket.timeout:
                print('timeout')


            if (ball_was) and (time() - noballstime > 1.0):
                self.lkmrelease()
                #print("OTPUSK")
            #if (ball_was) and (time() - noballstime > 6.0):
                #ball_loop = False
               # self.lkmrelease()
               # print("ballstop")
            if (time() - noballstimeFull > 50):
                ball_loop = False
                self.lkmrelease()

    def getBestBox(self, detected_boxes, cls , xyxy = [0, 0, 640, 640]):
        best_box = None
        # bestboxdistFactor = None
        ballexist = False
        no_time = None
        for box in detected_boxes:
            distFactor = self.checkDistance(box)
            Y = self.checkDistanceY(box)
            # X = self.checkDistanceX(box)
            if -180 < Y < 300 and xyxy[0] <= (box.xyxy[0][0]+box.xyxy[0][2])/2 <= xyxy[2] and xyxy[1] <= (box.xyxy[0][1] + box.xyxy[0][3])/2 <= xyxy[3]:
                if box.cls == cls and not ballexist:

                    result = self.confirmExisting(box)

                    confirmed = result[0]
                    box = result[1]
                    if confirmed:
                        best_box = box
                        # bestboxdistFactor= distFactor
                        ballexist = True
                        no_time = time()
                elif box.cls == cls and box.conf > best_box.conf and ballexist:
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
    def SpiritLoop1(self):
        spirit_loop = True
        nospirittime = time()
        maxmousemove = [0,0]

        while (spirit_loop):

            self.getNextFrame()

            if self.blackScreenDetect():
                self.send_message_telega(f"{time() -nospirittime} sec, VAS ZABANISHILI or VAS KICKNULO Vo vremya dobivaniya")
                self.stop = True
                break
            ###
            Prediction = self.model.predict(source=self.img, device=0, conf=0.2, iou=0.2)
            # print(Prediction[0].boxes.xyxy)

            detected_boxes = Prediction[0].boxes

            # debug the loop rate
            # print('FPS {}'.format(1 / (time() - loop_time)))
            # loop_time = time()
            print("i will check")
            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 1)
                if not results is None:
                    best_box = results[0]
                    result = self.MouseMove(best_box, currentMousemove=maxmousemove,limit=450)
                    maxmousemove = result[1]
                    sleep(0.3)
                    if self.spiritdetect():
                        sleep(1.2)
                        self.lkmpress()
                        holdtime = time()
                        sleep(1.2)
                        print("click")
                        while self.spiritdetect():   #time() - nospirittime < 3
                            sleep(0.1)
                            #result = self.confirmExisting(best_box, precision=0.3, conf=0.4)
                            #confirmed = result[0]
                           # if confirmed:
                           #     nospirittime = time()
                           # if (time() - holdtime > 26.0):
                           #     break;

                        spirit_loop = False

                sleep(0.05)
                print("release")
                self.lkmrelease()
            if time() - nospirittime > 20:
                spirit_loop = False
            if not spirit_loop:
                for _ in range(self.movecounter):
                    sleep(0.25)
                    self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                    self.mousereturn[0] = 0
                    self.mousereturn[1] = 0
                    self.hold_and_release_sleep(self.moveback, 1)
                    sleep(1)
                    self.movecounter=0

    def SpiritLoop(self):
        spirit_loop = True
        nospirittime = time()
        predictedtime = time()
        maxmousemove = [0,0]
        canpress = False
        detected = False
        while (spirit_loop):

            self.getNextFrame()
            if self.checklowmana():
                print("LOWMANA")
                self.restart = True
                self.gosave()
                return False
            if self.blackScreenDetect():
                self.send_message_telega(f"{time() -nospirittime} sec, VAS ZABANISHILI or VAS KICKNULO Vo vremya dobivaniya")
                self.stop = True
                break
            ###
            try:
                command = client_socket.recv(1024)
                command = command.decode()
                print(f"{command} received in spiritloop")
                if int(command) == 3:
                    self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                    self.mousereturn[0] = 0
                    self.mousereturn[1] = 0
                    sleep(random.uniform(0.4, 1.2))
                    self.fastselfcast(self.barrier, 4.5)
                    self.fastselfcast(self.kau, 4)
                    # self.hold_and_release_sleep(self.moveback, 1.8)
                    #self.hold_and_release_sleep(self.moveright, 1)
                    #sleep(1)
                    #self.hold_and_release_sleep(self.moveleft, 1)
                    sleep(0.7)
                if int(command) != 2 and int(command) < 10:
                    spirit_loop = False
                else:
                    canpress= True
            except socket.timeout:
                print('timeout')
            Prediction = self.model.predict(source=self.img, device=0, conf=0.2, iou=0.2)
            # print(Prediction[0].boxes.xyxy)

            detected_boxes = Prediction[0].boxes

            # debug the loop rate
            # print('FPS {}'.format(1 / (time() - loop_time)))
            # loop_time = time()
            print("i will check")
            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 1)
                if not results is None:
                    predictedtime = time()
                    best_box = results[0]
                    result = self.MouseMove(best_box, currentMousemove=maxmousemove, limit =600)
                    maxmousemove = result[1]
                    sleep(0.3)
                    if self.spiritdetect():
                        nospirittime=time()
                        print("click")
                        detected = True

                        try:
                            command = client_socket.recv(1024)
                            command = command.decode()
                            print(command)
                            if int(command) == 3:
                                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                                self.mousereturn[0] = 0
                                self.mousereturn[1] = 0
                                sleep(random.uniform(0.4, 1.2))
                                self.fastselfcast(self.barrier, 4.5)
                                self.fastselfcast(self.kau, 4)
                                # self.hold_and_release_sleep(self.moveback, 1.8)
                                #self.hold_and_release_sleep(self.moveright, 1)
                                #sleep(1)
                                #self.hold_and_release_sleep(self.moveleft, 1)
                            if int(command) == 2:
                                canpress = True
                            elif int(command) != 2 and int(command) < 10:
                                spirit_loop = False

                        except socket.timeout:
                            print('timeout')
                        if canpress:
                            self.lkmpress()

                        while self.spiritdetect():
                            if not canpress:
                                try:
                                    command = client_socket.recv(1024)
                                    command = command.decode()
                                    print(command)
                                    if int(command) == 3:
                                        self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                                        self.mousereturn[0] = 0
                                        self.mousereturn[1] = 0
                                        sleep(random.uniform(0.4, 1.2))
                                        self.fastselfcast(self.barrier, 4.5)
                                        self.fastselfcast(self.kau, 4)
                                        # self.hold_and_release_sleep(self.moveback, 1.8)
                                        #self.hold_and_release_sleep(self.moveright, 1)
                                        #sleep(1)
                                        #self.hold_and_release_sleep(self.moveleft, 1)
                                    if int(command) == 2:
                                        canpress = True
                                    elif int(command) != 2 and int(command) < 10:
                                        spirit_loop = False
                                except socket.timeout:
                                    print('timeout')
                            if canpress:
                                self.lkmpress()
                            if self.blackScreenDetect():
                                self.send_message_telega(
                                    f"{time() - nospirittime} sec, VAS ZABANISHILI or VAS KICKNULO Vo vremya dobivaniya")
                                self.stop = True
                                break
                            if self.checklowmana():
                                print("LOWMANA")
                                self.restart = True
                                self.gosave()
                                return False
                            if self.lkmspam and canpress:
                                self.lkmrelease()
                                sleep(0.001)
                                self.lkmpress()
                                sleep(0.115)
                            sleep(0.1)

                        print("release")
                        self.lkmrelease()


                            #result = self.confirmExisting(best_box, precision=0.3, conf=0.4)
                            #confirmed = result[0]
                           # if confirmed:
                           #     nospirittime = time()
                           # if (time() - holdtime > 26.0):
                           #     break;
            try:
                command = client_socket.recv(1024)
                command = command.decode()
                print(command)
                print(f"{command} received in spiritloop")
                if int(command) == 3:
                    self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                    self.mousereturn[0] = 0
                    self.mousereturn[1] = 0
                    sleep(random.uniform(0.4, 1.2))
                    self.fastselfcast(self.barrier, 4.5)
                    self.fastselfcast(self.kau, 4)
                    # self.hold_and_release_sleep(self.moveback, 1.8)
                    #self.hold_and_release_sleep(self.moveright, 1)
                    #sleep(1)
                    #self.hold_and_release_sleep(self.moveleft, 1)
                if int(command) != 2 and int(command) < 10:
                    spirit_loop = False
                else:
                    canpress= True
            except socket.timeout:
                print('timeout')

            #if time() - nospirittime > 30:
               # spirit_loop = False
            #if time() - predictedtime > 6 and detected and canpress:
                #spirit_loop = False
            if time() - predictedtime > 3 and not detected:
                self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                self.mousereturn[0] = 0
                self.mousereturn[1] = 0
            if not spirit_loop:
                for _ in range(self.movecounter):
                    sleep(0.25)
                    self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
                    self.mousereturn[0] = 0
                    self.mousereturn[1] = 0
                    self.hold_and_release_sleep(self.moveback, 1)
                    sleep(1)
                    self.movecounter=0
        self.spiritCounter += 1
    def startLoop(self):
        sleep(2)
        start_loop = True
        startp=self.looptime
        nospirittime = time()
        released= True
        maxmousemove = [0 , 0]
        status_confirmed = True
        while (start_loop):


            self.getNextFrame()
            if self.blackScreenDetect():
                self.send_message_telega( f"VAS ZABANISHILI or VAS KICKNULO za {time()-startp} sec posle prizuva")
                self.stop = True
                break

            #print('FPS {}'.format(1 / (time() - loop_time)))
            #loop_time = time()

            while not status_confirmed:
                if (time() - self.looptime > 10):
                    self.restart = True
                    self.gosave()
                    return False
                if self.checknospirit():
                    self.release(self.moveback)
                    self.looptime = time()
                    sleep(0.8)
                    print(f"nospirit release")
                    return False
                if self.checkdrawnspirit():
                    print(f"spiritdrawned")
                    status_confirmed = True
                if self.checklowmana():
                    print("LOWMANA")
                    self.restart = True
                    self.gosave()
                    return False

                self.getNextFrame()
                if self.blackScreenDetect():
                    self.send_message_telega(f"VAS ZABANISHILI or VAS KICKNULO za {time() - startp} sec posle prizuva")
                    self.stop = True
                    break
                if (time()-self.looptime > self.MaxMoveBackTimer) and not released:
                    self.release(self.moveback)
                    self.looptime = time()
                    sleep(0.8)
                    print(f"{self.MaxMoveBackTimer} release")
                    released = True

            #if (time() - self.looptime > self.MaxMoveBackTimer) and not released:
                #self.release(self.moveback)
               # self.looptime = time()
                #sleep(0.8)
               # print(f"{self.MaxMoveBackTimer} release")
               # released = True


            Prediction = self.model.predict(source=self.img, device=0, conf=0.1, iou=0.2)
            detected_boxes = Prediction[0].boxes

            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 1)
                if (not results is None):
                    best_box, nospirittime = results
                    result = self.confirmExisting(best_box, conf=0.1, precision=0.99, i = 4)
                    confirmed = result[0]
                    best_box = result[1]

                    if confirmed and self.checkDistance(best_box) < 330 and (best_box.xyxy[0][2] - best_box.xyxy[0][0] < self.MaxSpiritSize or released):
                        if not released:
                            self.release(self.moveback)
                            self.looptime = time()
                            sleep(0.8)

                        result = self.MouseMove(best_box , currentMousemove=maxmousemove,limit= 600)
                        maxmousemove = result[1]
                        if result[0]:
                            return True



            if self.checklowmana():
                print("LOWMANA")
                self.restart = True
                self.gosave()
                return False
            try:
                command_with_time = client_socket.recv(1024)
                command = command_with_time.decode()

                # виконуємо команду та виводимо час її отримання
                print(f"Command '{command}' received in startloop")
                if int(command) > 0:
                    start_loop = False
                    self.lkmrelease()
                    print("Otpusk po prikazu")
                    return False
            except socket.timeout:
                print('timeout')
        return True
    def get_angles(self, aim_target, window_size=[640, 640], fov=(75, 75)):
        fov = (math.radians(fov[0]), math.radians(fov[1]))

        x_pos = aim_target[0] / (window_size[0] - 1)
        y_pos = aim_target[1] / (window_size[1] - 1)

        x_angle = math.atan((x_pos - 0.5) * 2 * math.tan(fov[0] / 2))
        y_angle = math.atan((y_pos - 0.5) * 2 * math.tan(fov[1] / 2))

        return (math.degrees(x_angle), math.degrees(y_angle))
    def mousemove(self, x, y, timer=0.01):

        n = int(max(abs(x) / 50, abs(y) / 50))

        if abs(x) > 0 or abs(y) > 0:
            if n > 0:
                xstep = int(x / n)
                ystep = int(y / n)
                xlast = x - xstep * n
                ylast = y - ystep * n
                timestep = timer / n
                for _ in range(n):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, xstep, ystep, 0, 0)
                    sleep(timestep)

                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, xlast, ylast, 0, 0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
                sleep(timer)
    def fastselfcast(self,spell,casttime):
        if self.stop:
            return False
        sleep(0.15)
        self.press(spell)
        sleep(0.1)
        #self.hold_and_release_sleep(self.moveleft,0.1)
        self.press(self.feint)
        sleep(0.15)
        #self.hold_and_release_sleep(self.moveright,0.1)
        self.press(self.selfcast)
        self.getNextFrame()
        if self.blackScreenDetect():
            self.send_message_telega(f"VAS ZABANISHILI or VAS KICKNULO Vo vremya selfcasta knopki {spell}")
            self.stop = True
            return False
        if self.checklowmana():
            print("LOWMANA")
            self.restart = True
            self.gosave()
            return False
        sleep(casttime/2)
        self.getNextFrame()
        if self.blackScreenDetect():
            self.send_message_telega(f"VAS ZABANISHILI or VAS KICKNULO Vo vremya selfcasta knopki {spell}")
            self.stop = True
            return False
        if self.checklowmana():
            print("LOWMANA")
            self.restart = True
            self.gosave()
            return False
        sleep(casttime / 2)
        return True
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
            return True
        else:
            return False
    def checkdrawnspirit(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[358:372, 223:253]
        if self.imgfind(img, "drawnthespirit.png", "drawnthespiritmask.png"):
            return True
        else:
            return False
    def checklowmana(self):

        # Read the images from the file
        bgrA=self.img[33:38, int(182 * self.lowmana_percentage)]
        result = True
        for i in range(5):
            bgr = bgrA[i]
            #print(bgr)
            if bgr[0]>=bgr[1]-1 and bgr[2]+1<bgr[0] and bgr[0]>4:
                result = False
        return result
    def gosave(self):
        print("TRYINGTOSTAYALIVE")
        if not self.SleepMode:
            self.send_message_telega("TRYING TO STAY ALIVe")
        self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
        self.mousereturn[0] = 0
        self.mousereturn[1] = 0
        for _ in range(6):
            self.getNextFrame()
            if self.blackScreenDetect():
                self.send_message_telega("VAS ZABANISHILI or VAS KICKNULO when trying to save")
                self.stop = True
                return False
            self.hold_and_release_sleep(self.moveback, self.savemovetimer/6)
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
                #if random.randint(1,10)>6:
                    #self.press("SPACEBAR")
                self.hold_and_release_sleep(self.moveright, 1)
                self.hold_and_release_sleep(self.moveleft, 1)

            self.stop = True
            return False
        for _ in range(120):
            sleep(self.savedelay/120)
            self.getNextFrame()
            if self.blackScreenDetect():
                self.send_message_telega("VAS ZABANISHILI or VAS KICKNULO when trying to save")
                self.stop = True
                return False
        for _ in range(6):
            self.hold_and_release_sleep(self.moveforward, self.savemovetimer/6)
            self.getNextFrame()
            if self.blackScreenDetect():
                self.send_message_telega("VAS ZABANISHILI or VAS KICKNULO when trying to save")
                self.stop = True
                return False
        self.justReturned = True
        return True
    def imgfind(self, large_image, small_img, mask, conf=0.6 ):

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
    def returning(self):
        sleep(0.1)
        # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -mousereturn[0], -mousereturn[1], 0, 0)
        print("ANGLES", self.mousereturn[0], self.mousereturn[1])
        self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
        self.mousereturn[0] = 0
        self.mousereturn[1] = 0
        sleep(0.3)
        self.hold_and_release_sleep(self.moveforward, self.movetime * self.MoveForwardMultiplier)
    def calibrate(self):
        print("CALIBRATION")
        client_socket.settimeout(120)
        startTime = time()
        while True:
            self.getNextFrame()
            if self.blackScreenDetect():
                self.send_message_telega("VAS ZABANISHILI or VAS KICKNULO")
                self.stop = True
            if self.stop:
                break
            if time() - startTime > 40:
                command = 0
                command_with_time = f"{command}".encode()
                client_socket.sendall(command_with_time)
                client_socket.settimeout(0.1)
                print("40sec timeout")
                return False
            Prediction = self.model.predict(source=self.img, device=0, conf=0.01, iou=0.2)
            detected_boxes = Prediction[0].boxes
            if len(detected_boxes) >= 1:
                results = self.getBestBox(detected_boxes, 1, xyxy = [0, 230 , 640, 420 ])
                if not results is None:
                    box = results[0]
                    #result = self.confirmExisting(box, conf=0.01, precision=0.9, i=5)
                    #confirmed = result[0]
                    #box = result[1]
                    #if confirmed:
                    print("Hoster found")

                    Xcenter = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
                    if Xcenter > 327:
                        print("move him left")
                        command = 2
                        command_with_time = f"{command}".encode()
                        client_socket.sendall(command_with_time)
                        sleep(1)
                        client_socket.recv(1024)
                        sleep(1)

                    elif Xcenter < 313:
                        print("move him right")
                        command = 1
                        command_with_time = f"{command}".encode()
                        client_socket.sendall(command_with_time)
                        sleep(1)
                        client_socket.recv(1024)
                        sleep(1)
                    else:
                        print("end")
                        command = 0
                        command_with_time = f"{command}".encode()
                        client_socket.sendall(command_with_time)
                        client_socket.settimeout(0.1)
                        return True
        print("somrthing wrong")
        client_socket.settimeout(0.1)
        return False
    def custom(self):




        #self.camera.start(region=(8+self.rect[0], 31+self.rect[1], 640+self.rect[0]-8, 640+self.rect[1]-31), target_fps=self.target_fps)
        self.getNextFrame()

        ###
        Prediction = self.model.predict(source=self.img, device=0, conf=0.6, iou=0.2, imgsz = 640)
        sleep(1)
        ###
        timer60power = time() - 60

        timer60 = time()-60
        while (True):
            print(f"Spirit № {self.spiritCounter}")
            # 10 pixels = 1.25degree
            self.lkmrelease()


            self.getNextFrame()
            if self.blackScreenDetect():
                self.send_message_telega(f"VAS ZABANISHILI or VAS KICKNULO Vo vremya obnovleniya barriera")
                self.stop = True
            if self.checklowmana():
                print("LOWMANA")
                self.restart = True
                self.gosave()
            while (True):
                try:
                    command_with_time = client_socket.recv(1024)
                    command = command_with_time.decode()

                    # виконуємо команду та виводимо час її отримання
                    print(f"Command '{command}' received")
                    if int(command) == 3:
                        sleep(random.uniform(0.4,1.0))
                        self.fastselfcast(self.barrier, 4.5)
                        self.fastselfcast(self.kau, 4)
                        self.rebuffCounter += 1
                        #self.hold_and_release_sleep(self.moveback, 1.8)
                        if self.rebuffCounter - self.lastAntiAFKmove > 15:
                            sleep(0.2)
                            self.hold_and_release_sleep(self.moveright,1)
                            sleep(0.7)
                            self.hold_and_release_sleep(self.moveleft, 1)
                            sleep(0.7)
                            self.lastAntiAFKmove = self.rebuffCounter
                    if int(command) == 4:
                        print('going to ballstage')
                        break
                    if int(command) == 99:
                        self.calibrate()
                except socket.timeout:
                    print('timeout')



            print("\n\nBALLLOOP\n\n")

            self.looptime = time()
            if self.stop:
                break
            if self.startLoop():
                self.BallLoop()
            if self.restart:
                self.restart = False
                self.returning()
                continue

            checkrebuff = time()-timer60power > 52
            if checkrebuff:
                while time()-timer60power < 53.1:
                    sleep(0.1)
                    self.getNextFrame()
                    if self.blackScreenDetect():
                        self.send_message_telega(
                            f"VAS ZABANISHILI or VAS KICKNULO pered buffom expel")
                        self.stop = True

                    if self.checklowmana():
                        print("LOWMANA")
                        self.restart = True
                        self.gosave()
                    print("wait until 4 sec of expel")
            if checkrebuff:
                self.fastselfcast(self.power, 6.5 )
                timer60power = time()
            #else:
                #self.fastselfcast(self.kau, 4)
            print("\n\nSPIRITLOOP\n\n")
            if self.stop:
                break
            self.SpiritLoop()
            if self.restart:
                self.restart = False
                continue
            if self.stop:
                break
            sleep(0.1)
            # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -mousereturn[0], -mousereturn[1], 0, 0)
            print("ANGLES", self.mousereturn[0], self.mousereturn[1])
            self.mousemove(int(-self.mousereturn[0]), int(-self.mousereturn[1]))
            self.mousereturn[0] = 0
            self.mousereturn[1] = 0
            #self.hold_and_release_sleep(self.moveforward, 1.8)
            sleep(0.3)

            '''
            for _ in range(320):
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 10, 0, 0, 0)
                sleep(0.02)
            sleep(10.1)
            '''

        self.camera.stop()
        client_socket.close()
        print('Done.')
        pass


def run():
    script_class = ClassName()  # инициализация класса (сменить название на актуальное)
    script_class.custom()


if __name__ == "__main__":
    run()

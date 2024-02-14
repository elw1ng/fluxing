import sys
from time import sleep
from time import time
from threading import Thread
import fLUX

class ClassName(fLUX.ClassName):  # Название класса (должен отличаться от других названий скриптов)

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
        Prediction = self.model.predict(source=self.img, device=0, conf=0.6, iou=0.2, imgsz=640, show=False, verbose=False)
        sleep(1)
        ###
        timer60power = time() - 60
        k = 0
        timer60 = time() - 60
        while (True):
            while self.reconnection:
                sleep(1)
                if time()-timer60 > 1200:
                    self.send_message_telega("Unable to coonect to server 20 mins")
                    sys.exit()
            rebuffed = False
            # 10 pixels = 1.25degree
            self.lkmrelease()
            if self.stop:
                break
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
                if (time() - timer60 > 47.5 - extrabarriertime):
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
                    self.fastselfcast(self.barrier, 4.5)
                    # if self.checklowmana(percentage=0.36):
                    self.fastselfcast(self.kau, 4.1)

                self.fastselfcast(self.summon, 6.2)
                if self.mover is None:
                    self.mover = Thread(target=self.MoveBack, args=())
                    self.mover.start()
                else:
                    self.mover.join()
                    self.mover = Thread(target=self.MoveBack, args=())
                    self.mover.start()
                startp = time()
                self.looptime = startp

                print("\n\nSTARTLOOP\n\n")

                started = self.startLoop()
                if self.restart:
                    self.restart = False
                    self.returning()
                    continue
                self.movetime = self.looptime - startp
                if (not started):
                    sleep(1.6)
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
                    self.returning()
                    #sleep(1)
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
            print("\n\nBALLLOOP\n\n")

            spiritdone = False
            firsttime = True
            while not spiritdone:
                self.looptime = time()
                if self.stop:
                    break

                self.BallLoop(firsttime = firsttime,maxnoballtimer=1.6)
                firsttime = False
                if self.restart:
                    self.restart = False
                    break

                checkrebuff = time() - timer60power > 60
                if checkrebuff:
                    while time() - timer60power < 60.04:
                        self.getNextFrame()
                        Prediction = self.model.predict(source=self.img, device=0, conf=0.3, iou=0.2)
                        # print(Prediction[0].boxes.xyxy)

                        detected_boxes = Prediction[0].boxes

                        # debug the loop rate
                        # print('FPS {}'.format(1 / (time() - loop_time)))
                        # loop_time = time()
                        print("i will check")
                        if len(detected_boxes) >= 1:
                            results = self.getBestBox(detected_boxes, 0)
                            if not results is None:
                                bestbox, _ = results
                                result = self.confirmExisting(bestbox, conf=0.3, i=2, precision=0.99)
                                confirmed = result[0]
                                if confirmed:
                                    continue
                        if self.blackScreenDetect():
                            self.send_message_telega(
                                f"VAS ZABANISHILI or VAS KICKNULO pered buffom expel")
                            self.stop = True

                        if self.lowmana:
                            print("LOWMANA")
                            self.restart = True
                            self.gosave()
                        print("wait until 4 sec of expel")
                if checkrebuff:
                    #sleep(0.07)
                    timer60power = time()
                    self.fastselfcast(self.power, 5.65)

                if not checkrebuff and not rebuffed:
                    #sleep(0.07)
                    self.lkmrelease()
                    self.press(self.kau)
                    sleep(4.1)
                #else:
                    #self.fastselfcast(self.kau, 4)
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

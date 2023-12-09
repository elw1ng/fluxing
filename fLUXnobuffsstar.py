import random
import sys
from time import sleep
from time import time
from threading import Thread
import fLUX

class ClassName(fLUX.ClassName):  # Название класса (должен отличаться от других названий скриптов)

    def custom(self):
        povorotX = int(10 * random.uniform(200, 225) / 1.125 * 90 / 60)
        negative = random.randint(1,2)
        if negative ==1:
            povorotX = -povorotX
        else:
            pass

        sleep(1)
        self.mousemove(int(povorotX / 2), 0)
        if self.checker is None:
            self.checker = Thread(target=self.checkers, args=())
            self.checker.start()
        notified = False
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
                if self.mover is not None:
                    self.mover.join()
                self.fastselfcast(self.summon, 6.2,strafe=True)
                self.movecounter=0
                if self.mover is None:
                    self.mover = Thread(target=self.MoveBack(), args=())
                    self.mover.start()
                else:
                    self.mover.join()
                    self.mover = Thread(target=self.MoveBack(), args=())
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
                    sleep(0.8)
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
            print("\n\nBALLLOOP\n\n")

            spiritdone = False
            firsttime = True
            while not spiritdone:
                self.looptime = time()
                if self.stop:
                    break
                #self.lkmrelease()
                self.strafe = True
                if self.mover is None:
                    self.mover = Thread(target=self.strafing, args=(True,))
                    self.mover.start()
                else:
                    self.mover.join()
                    self.mover = Thread(target=self.strafing, args=(True,))
                    self.mover.start()
                self.BallLoop(firsttime = firsttime,maxnoballtimer=1)
                self.strafe = False
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
                    if self.mover is not None:
                        self.strafe = False
                        self.mover.join()
                    self.fastselfcast(self.power, 4.6,strafe=True)

                else:
                    # sleep(0.07)
                    if self.mover is not None:
                        self.strafe= False
                        self.mover.join()
                    self.fastselfcast(self.kau, 3.8,strafe=True)

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

                # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -mousereturn[0], -mousereturn[1], 0, 0)
            if self.t is not None:
                self.t.join()
                self.t = None
                sleep(1 / 35)
            print("ANGLES", self.mousereturn[0], self.mousereturn[1])
            self.mousemove(int(-self.mousereturn[0]+povorotX), int(-self.mousereturn[1]))
            self.mousereturn[0] = 0
            self.mousereturn[1] = 0



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

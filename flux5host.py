import threading
import sys
import torch
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
#import pyautogui
import copy
from pyduino_mk.constants import *
from pyduino_mk import Arduino
import numpy as np
import keyboard

# отримуємо IP-адресу хоста
host_ip = socket.gethostbyname(socket.gethostname())
#host_ip = "193.33.38.56"
print("Host IP address:", host_ip)

# створюємо сокет та встановлюємо його для прослуховування
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, 12345))
server_socket.listen(1)

print("Waiting for connections...")

# очікуємо на підключення першого клієнта
client1_socket, client1_address = server_socket.accept()
print("Client 1 connected from", client1_address)

while True:
    if keyboard.is_pressed('r'):
        print("REBUFF")
        command = 3
        command_with_time = f"{command}".encode()
        client1_socket.sendall(command_with_time)

        sleep(2)
    if keyboard.is_pressed('e'):
        print("ballloop")
        command = 4
        command_with_time = f"{command}".encode()
        client1_socket.sendall(command_with_time)

        sleep(2)
    if keyboard.is_pressed('f'):
        print("spiritloop")
        command = 2
        command_with_time = f"{command}".encode()
        client1_socket.sendall(command_with_time)

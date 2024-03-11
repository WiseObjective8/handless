from typing import Mapping
import cv2 as cv
import mediapipe as mp
import matplotlib.pyplot as plt
import pyautogui as pa
import mouse
import ctypes
from threading import *


class Reader(Thread):
    def __init__(self, cam=0) -> None:
        super().__init__(target=self.read)
        self.w, self.h = pa.size()
        self.cam = cv.VideoCapture(cam)
        self.isavailable = self.cam.isOpened()
        if self.isavailable:
            self.start()
        else:
            self.exit()

    def read(self):
        while self.isavailable:
            _, self.frm = self.cam.read()
            if _:
                self.frm = cv.flip(self.frm, -1)
            if KeyboardInterrupt:
                self.exit()

    def exit(self):
        self.isavailable = False
        self.join()


class Viewer(Thread):
    def __init__(self) -> None:
        frm = None
        super().__init__(target=self.view, args=(self,frm,))
        self.isempty =  False
        if not self.isempty:
            self.start()
        else:
            self.exit()

    def view(self,frm): 
        self.isempty = bool(frm)
        cv.imshow("",frm)
        ...
    def exit(self): 
        self.isempty = True
        self.join()
        ...

x = Reader()
y = Viewer()

while x.is_alive():
    y.view(x.frm)
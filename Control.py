try:
    import cv2 as cv
    import mediapipe as mp
    import matplotlib.pyplot as plt
    import pyautogui as pa
except:
    print("Error, please install all the required packages")


class Mouse:
    def __init__(self): 
        self.width, self.height = ...
        ...
    def camera(self): ...
    def mark_nose(self): ...
    def visualize(): ...
    def move(self): ...
    def click(self): ...
    def run(self): ...
    def stop(self): ...
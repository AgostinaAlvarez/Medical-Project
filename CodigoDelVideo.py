import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image,ImageTk
import imutils
import math


def Log_Biometric():
    global cap,lblVideo

    if cap is not None:
        ret,frame = cap.read()

        #frame = imutils.resize(frame, width=1280)

        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image = img)
        lblVideo.image = img
        lblVideo.after(10, Log_Biometric)
    else:
        cap.release()



def Log():
    global pantalla2, lblVideo, cap
    print('Entrar')

    pantalla2 = Toplevel(pantalla)
    pantalla2.title('Login Biometric')
    pantalla2.geometry("1280x720")

    lblVideo = Label(pantalla2)
    lblVideo.place(x=0,y=0)

    cap = cv2.VideoCapture(0)
    #cap.set(3,1280)
    #cap.set(4,1280)


def Sign():
    print('Crear usuario')

info = []


pantalla = Tk()
pantalla.title('Face recognition')
pantalla.geometry("1280x720")


BtnReg = Button(pantalla, text='Crear usuario', command=Sign)
BtnReg.place(x=0,y=0)
BtnSign = Button(pantalla, text='Entrar', command=Log)
BtnSign.place(x=0,y=30)


pantalla.mainloop()


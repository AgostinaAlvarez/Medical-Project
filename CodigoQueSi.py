import cv2
import tkinter as tk
from PIL import Image, ImageTk

def update_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label_video.imgtk = photo
        label_video.configure(image=photo)
        label_video.after(10, update_video)  # Actualiza cada 10 milisegundos

root = tk.Tk()
root.title("Captura de cámara con Tkinter y OpenCV")

label_video = tk.Label(root)
label_video.pack()

cap = cv2.VideoCapture(0)  # Abre la cámara (índice 0)

update_video()  # Inicia la actualización del video

root.mainloop()


#####################

import cv2
import tkinter as tk
from PIL import Image, ImageTk



def open_camera_window():
    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            label_video.imgtk = photo
            label_video.configure(image=photo)
            label_video.after(10, update_video)  # Actualiza cada 10 milisegundos


    new_window = tk.Toplevel(root)
    new_window.title("Captura de cámara con Tkinter y OpenCV")

    label_video = tk.Label(new_window)
    label_video.pack()

    cap = cv2.VideoCapture(0)  # Abre la cámara (índice 0)

    update_video()  # Inicia la actualización del video en la nueva ventana



root = tk.Tk()
root.title("Ventana Principal")
root.geometry("600x400")  # Establece las dimensiones de la ventana principal
button = tk.Button(root, text="Abrir cámara", command=open_camera_window)
button.pack()

root.mainloop()


############# codigo de tkinter que si funnciona

import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image,ImageTk
import imutils
import math


def update_video():
    global lblVideo, cap
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        lblVideo.imgtk = photo
        lblVideo.configure(image=photo)
        lblVideo.after(10, update_video)  # Actualiza cada 10 milisegundos

def open ():
    global lblVideo,cap
    print('abrir')
    pantalla2 = Toplevel(pantalla)
    pantalla2.title('biometrico')

    lblVideo = Label(pantalla2)
    lblVideo.pack()

    cap = cv2.VideoCapture(0)
    update_video()

pantalla = Tk()

pantalla.title('Pantalla prinicipal')
pantalla.geometry("1200x720")

boton = Button(pantalla,text='abrir camara',command=open)
boton.pack()


pantalla.mainloop()
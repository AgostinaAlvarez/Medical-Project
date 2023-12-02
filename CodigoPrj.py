
import cv2
from PIL import Image, ImageTk

import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image,ImageTk
import imutils
import math


def open_camera_window():
    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if ret == True :
                res = FaceMesh.process(frameRGB)

                if res.multi_face_landmarks :
                    for rostros in res.multi_face_landmarks:
                        mpDraw.draw_landmarks(frame,rostros, FacemeshObject.FACE_CONNECTIONS, ConnfigDraw, ConnfigDraw)

            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            label_video.imgtk = photo
            label_video.configure(image=photo)
            label_video.after(10, update_video)  # Actualiza cada 10 milisegundos


    new_window = Toplevel(root)
    new_window.title("Captura de cámara con Tkinter y OpenCV")
    new_window.geometry("1200x720")
    label_video = Label(new_window)
    label_video.pack()

    cap = cv2.VideoCapture(0)  # Abre la cámara (índice 0)

    update_video()  # Inicia la actualización del video en la nueva ventana


offsety = 30
offsetx = 20


confThreshold = 0.5

mpDraw = mp.solutions.drawing_utils

ConnfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

#objeto malla

FacemeshObject = mp.solutions.face_mesh

FaceMesh = FacemeshObject.FaceMesh(max_num_faces=1)

#detector de rostro

FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)


root = Tk()
root.title("Ventana Principal")
root.geometry("600x400")  # Establece las dimensiones de la ventana principal
button = Button(root, text="Abrir cámara", command=open_camera_window)
button.pack()

root.mainloop()


#####################


import tkinter as tk
def pantalla_principal():
    # Función que muestra la pantalla principal
    pantalla1.pack()
    pantalla2.pack_forget()  # Oculta la pantalla 2 si estaba visible

def cambiar_pantalla():
    # Función que cambia de pantalla
    pantalla1.pack_forget()  # Oculta la pantalla 1
    pantalla2.pack()  # Muestra la pantalla 2

def volver_atras():
    # Función que permite regresar a la pantalla principal desde la pantalla 2
    pantalla_principal()

root = tk.Tk()
root.title("Cambiar Pantallas")

# Crear los contenidos de las pantallas
pantalla1 = tk.Frame(root)
label_pantalla1 = tk.Label(pantalla1, text="Pantalla 1")
label_pantalla1.pack()

pantalla2 = tk.Frame(root)
label_pantalla2 = tk.Label(pantalla2, text="Pantalla 2")
label_pantalla2.pack()

# Botón para cambiar entre pantallas
button_cambiar = tk.Button(root, text="Cambiar Pantalla", command=cambiar_pantalla)
button_cambiar.pack()

# Botón para volver atrás desde la pantalla 2
button_volver = tk.Button(pantalla2, text="Volver Atrás", command=volver_atras)
button_volver.pack()

# Mostrar la pantalla principal por defecto
pantalla_principal()

root.mainloop()


#################
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock

import cv2
import mediapipe as mp
from PIL import Image as PILImage
from io import BytesIO
import numpy as np


class CameraApp(App):
    def build(self):
        self.new_window = BoxLayout(orientation='vertical')
        self.label_video = Image()
        self.new_window.add_widget(self.label_video)

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,
                                                    min_detection_confidence=0.5)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_video, 1.0 / 30.0)  # Actualiza cada 1/30 segundos

        return self.new_window

    def update_video(self, dt):
        ret, frame = self.capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Procesamiento de Mediapipe para detección facial
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frameRGB)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for ix, landmark in enumerate(face_landmarks.landmark):
                        h, w, c = frame.shape
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.label_video.texture = texture

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    CameraApp().run()


#######
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
import mediapipe as mp
from kivy.graphics.texture import Texture
import numpy as np


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        button = Button(text='Abrir cámara', on_press=self.switch_to_camera)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_camera(self, instance):
        self.manager.current = 'camera'


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.label_video = Image()
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label_video)
        self.add_widget(layout)

    def on_enter(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,
                                                    min_detection_confidence=0.5)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_video, 1.0 / 30.0)  # Actualiza cada 1/30 segundos

    def update_video(self, dt):
        ret, frame = self.capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frameRGB)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for ix, landmark in enumerate(face_landmarks.landmark):
                        h, w, c = frame.shape
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.label_video.texture = texture

    def on_leave(self):
        self.capture.release()


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        main_screen = MainScreen(name='main')
        camera_screen = CameraScreen(name='camera')
        sm.add_widget(main_screen)
        sm.add_widget(camera_screen)
        return sm


if __name__ == '__main__':
    MyApp().run()

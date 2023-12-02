
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
    def on_closing():
        cap.release()  # Libera los recursos de la cámara al cerrar la ventana
        new_window.destroy()

    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if ret == True :
                res = FaceMesh.process(frameRGB)
                px = []
                py = []
                lista = []

                if res.multi_face_landmarks :
                    #estraer face mash
                    for rostros in res.multi_face_landmarks:
                        #Draw
                        mpDraw.draw_landmarks(frame,rostros, FacemeshObject.FACE_CONNECTIONS, ConnfigDraw, ConnfigDraw)
                        #extraer informacion

                        for id, puntos in enumerate(rostros.landmark):
                            #info img
                            al, an, c = frame.shape
                            x, y = int(puntos.x * an), int(puntos.y * al)
                            px.append(x)
                            py.append(y)
                            lista.append([id, x, y])

                            #existen 468 KeyPoints
                            if len(lista) == 468:
                                #ojo derecho
                                x1, y1 = lista[145][1:]
                                x2, y2 = lista[159][1:]
                                longitud1 = math.hypot(x2-x1, y2-y1)


                                # ojo izquierdo
                                x3, y3 = lista[374][1:]
                                x4, y4 = lista[386][1:]
                                longitud2 = math.hypot(x3 - x4, y3 - y4)

                                #cv2.circle(frame, (x1, y1), 2, (255, 0, 0), cv2.FILLED)
                                #cv2.circle(frame, (x2, y2), 2, (255, 0, 0), cv2.FILLED)

                                #cv2.circle(frame, (x3, y3), 2, (255, 0, 0), cv2.FILLED)
                                #cv2.circle(frame, (x4, y4), 2, (255, 0, 0), cv2.FILLED)

                                #print()

                                faces = detector.process(frameRGB)

                                if faces.detections is not None:
                                    for face in faces.detections:
                                        score = face.score
                                        score = score[0]
                                        bbox = face.location_data.relative_bounding_box

                                        #Threshold
                                        if score > confThreshold:
                                            #print('hola')
                                            xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                            xi, yi, anc, alt = int(xi * an), int(yi * al), int(anc * an), int(alt * al)

                                            offsetan = (offsetx/100) * anc
                                            xi = int(xi - int(offsetan/2))
                                            anc = int(anc + offsetan)

                                            offsetal = (offsety / 100) * alt
                                            yi = int(yi - int(offsetal / 2))
                                            alt = int(alt + offsetal)

                                            if xi < 0 : xi = 0
                                            if yi < 0 : yi = 0
                                            if anc < 0 : anc = 0
                                            if alt < 0 : alt = 0

                                            if step == 0:
                                                #Draw
                                                cv2.rectangle(frame, (xi, yi, anc, alt), (255, 0, 255), 2)

                                                #imagen
                                                als0, ans0, c = Alert1.shape
                                                frame[50:50 + als0, 50:50 + ans0] = Alert1

                                                als1, ans1, c = Step1.shape
                                                frame[50:50 + als1, 1030:1030 + ans1] = Step1

                                                als2, ans2, c = Step2.shape
                                                frame[270:270 + als2, 1030:1030 + ans2] = Step2

                                            #draw rectangulo tester
                                            #cv2.rectangle(frame, (xi, yi, anc, alt), (255, 255, 255), 2)


            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            label_video.imgtk = photo
            label_video.configure(image=photo)
            label_video.after(10, update_video)  # Actualiza cada 10 milisegundos

    new_window = Toplevel(root)
    new_window.title("Captura de cámara con Tkinter y OpenCV")
    new_window.geometry("1200x720")
    new_window.protocol("WM_DELETE_WINDOW", on_closing)  # Captura el evento de cierre de ventana

    label_video = Label(new_window)
    label_video.pack()

    cap = cv2.VideoCapture(0)  # Abre la cámara (índice 0)

    update_video()  # Inicia la actualización del video en la nueva ventana


parpadeo = False
conteo = 0
muestra = 0
step = 0

offsety = 30
offsetx = 20

confThreshold = 0.5


#read images

Alert1 = cv2.imread("/Users/mac/Desktop/proyecto-medical-history/SetUp/alert0.png")
Step1 = cv2.imread("/Users/mac/Desktop/proyecto-medical-history/SetUp/step1.png")
Step2 = cv2.imread("/Users/mac/Desktop/proyecto-medical-history/SetUp/step2.png")


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

from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
import mediapipe as mp
from kivy.graphics.texture import Texture
import numpy as np
import math



class SearchUserCamera(Screen):
    def __init__(self, **kwargs):
        super(SearchUserCamera, self).__init__(**kwargs)
        self.back_button = Button(text='volver atras',size_hint=(1,None),height=100)
        self.back_button.bind(on_release=self.switch_screen_back)
        self.label_video = Image()

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.back_button)
        layout.add_widget(self.label_video)
        self.add_widget(layout)

    def on_enter(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_video, 1.0 / 30.0)  # Actualiza cada 1/30 segundos

    def update_video(self, dt):

        global parpadeo,conteo

        ret, frame = self.capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if ret == True:
                res = self.face_mesh.process(frameRGB)
                px = []
                py = []
                lista = []

                if res.multi_face_landmarks:
                    for rostros in res.multi_face_landmarks:
                        #Draw
                        mpDraw.draw_landmarks(frame,rostros, FacemeshObject.FACE_CONNECTIONS, ConnfigDraw, ConnfigDraw)

                        for id, puntos in enumerate(rostros.landmark):
                            #info img
                            al, an, c = frame.shape
                            x, y = int(puntos.x * an), int(puntos.y * al)
                            px.append(x)
                            py.append(y)
                            lista.append([id, x, y])

                            #existen 468 KeyPoints
                            if len(lista) == 468:
                                #ojo derecho coordenadas
                                #---superior
                                x1, y1 = lista[145][1:]
                                #---inferior
                                x2, y2 = lista[159][1:]
                                longitud1 = math.hypot(x2-x1, y2-y1)


                                #ojo izquierdo coordenadas
                                #---superior
                                x3, y3 = lista[374][1:]
                                #---inferior
                                x4, y4 = lista[386][1:]
                                longitud2 = math.hypot(x3 - x4, y3 - y4)

                                #ojo derecho draw
                                cv2.circle(frame, (x1, y1), 2, (255, 0, 0), cv2.FILLED)
                                cv2.circle(frame, (x2, y2), 2, (255, 0, 0), cv2.FILLED)

                                #ojo izquierdo draw
                                cv2.circle(frame, (x3, y3), 2, (255, 0, 0), cv2.FILLED)
                                cv2.circle(frame, (x4, y4), 2, (255, 0, 0), cv2.FILLED)

                                #parietales coordenadas
                                #---parietal derecho
                                x5, y5 = lista[139][1:]
                                #---parietal izquierdo
                                x6, y6 = lista[368][1:]

                                #cejas coordenadas
                                # --- ceja derecha
                                x7, y7 = lista[70][1:]
                                # --- ceja izquierda
                                x8, y8 = lista[300][1:]

                                #parietales draw
                                cv2.circle(frame, (x5, y5), 2, (0, 255, 0), cv2.FILLED)
                                cv2.circle(frame, (x6, y6), 2, (0, 255, 0), cv2.FILLED)

                                #cejas draw
                                cv2.circle(frame, (x7, y7), 4, (0, 0, 255), cv2.FILLED)
                                cv2.circle(frame, (x8, y8), 4, (0, 0, 255), cv2.FILLED)

                                faces = detector.process(frameRGB)

                                if faces.detections is not None:
                                    for face in faces.detections:
                                        score = face.score
                                        score = score[0]
                                        bbox = face.location_data.relative_bounding_box

                                        # Threshold
                                        if score > confThreshold:
                                            # print('hola')
                                            xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                            xi, yi, anc, alt = int(xi * an), int(yi * al), int(anc * an), int(alt * al)

                                            offsetan = (offsetx / 100) * anc
                                            xi = int(xi - int(offsetan / 2))
                                            anc = int(anc + offsetan)

                                            offsetal = (offsety / 100) * alt
                                            yi = int(yi - int(offsetal / 2))
                                            alt = int(alt + offsetal)

                                            if xi < 0: xi = 0
                                            if yi < 0: yi = 0
                                            if anc < 0: anc = 0
                                            if alt < 0: alt = 0

                                            if step == 0:
                                                # Draw
                                                cv2.rectangle(frame, (xi, yi, anc, alt), (255, 0, 255), 2)

                                                # imagen
                                                als0, ans0, c = Alert1.shape
                                                frame[50:50 + als0, 50:50 + ans0] = Alert1

                                                als1, ans1, c = Step1.shape
                                                frame[50:50 + als1, 1030:1030 + ans1] = Step1

                                                als2, ans2, c = Step2.shape
                                                frame[270:270 + als2, 1030:1030 + ans2] = Step2

                                                if x7 > x5 and x8 < x6:
                                                    alcheck, ancheck, c = Check.shape

                                                    frame[165:165 + alcheck, 1105:1105 + ancheck] = Check

                                                    #print('longitud 1')
                                                    #print(longitud1)

                                                    if longitud1 <= 20 and longitud2 <= 20 and parpadeo == False :
                                                        print('parpadeo')
                                                        parpadeo = True
                                                        if conteo == 3:
                                                            conteo = 3
                                                        else:
                                                            conteo = conteo + 1

                                                    elif longitud1 > 20 and longitud2 > 20 and parpadeo == True:
                                                        print('no parpadeo')
                                                        parpadeo = False


                                                    cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070,375), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)

                                                    if conteo >= 3:
                                                        alcheck, ancheck, c = Check.shape
                                                        frame[385:385 + alcheck, 1105:1105 + ancheck] = Check

                                                        cv2.rectangle(frame, (xi, yi, anc, alt), (0, 255, 0), 2)


            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.label_video.texture = texture

    def on_leave(self):
        self.capture.release()


    def switch_screen_back(self, instance):
        self.manager.current = 'search_user_screen'

mpDraw = mp.solutions.drawing_utils
FacemeshObject = mp.solutions.face_mesh
FaceMesh = FacemeshObject.FaceMesh(max_num_faces=1)
ConnfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
parpadeo = False
conteo = 0
muestra = 0
step = 0

offsety = 30
offsetx = 20

confThreshold = 0.5

#detector de rostro
FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)


Alert1 = cv2.imread("/Users/mac/Desktop/proyecto-medical-history/SetUp/alert0.png")
Step1 = cv2.imread("/Users/mac/Desktop/proyecto-medical-history/SetUp/Paso0.png")
Step2 = cv2.imread("/Users/mac/Desktop/proyecto-medical-history/SetUp/Paso1.png")
Check = cv2.imread("/Users/mac/Desktop/proyecto-medical-history/SetUp/check.png")
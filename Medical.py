

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
import mediapipe as mp
from kivy.graphics.texture import Texture
import math


class MainScreen(Screen):
    def switch_to_camera(self):
        self.manager.current = 'camera'


class CameraScreen(Screen):
    def on_enter(self):

        self.texture = Texture.create(size=(1, 1))  # Crear un objeto Texture vacío al inicio

        self.px = []
        self.py = []
        self.lista = []

        self.FaceObject = mp.solutions.face_detection

        self.detector = self.FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)

        self.label_video = self.ids.label_video
        self.FacemeshObject = mp.solutions.face_mesh
        self.FaceMesh = self.FacemeshObject.FaceMesh(max_num_faces=1)
        self.mpDraw = mp.solutions.drawing_utils
        self.ConnfigDraw = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_video, 1.0 / 30.0)  # Actualiza cada 1/30 segundos

    def update_video(self, dt):
        ret, frame = self.capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.FaceMesh.process(frameRGB)

            if results.multi_face_landmarks:
                for rostros in results.multi_face_landmarks:

                    self.mpDraw.draw_landmarks(frame, rostros, self.FacemeshObject.FACE_CONNECTIONS, self.ConnfigDraw, self.ConnfigDraw)

                    for id, puntos in enumerate(rostros.landmark):
                        # info img
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        self.px.append(x)
                        self.py.append(y)
                        self.lista.append([id, x, y])

                        # existen 468 KeyPoints
                        if len(self.lista) == 468:
                            print('hay')
                            # ojo derecho
                            x1, y1 = self.lista[145][1:]
                            x2, y2 = self.lista[159][1:]
                            longitud1 = math.hypot(x2 - x1, y2 - y1)
                            # ojo izquierdo
                            x3, y3 = self.lista[374][1:]
                            x4, y4 = self.lista[386][1:]
                            longitud2 = math.hypot(x3 - x4, y3 - y4)

                            cv2.circle(frame, (x1, y1), 2, (255, 0, 0), cv2.FILLED)
                            cv2.circle(frame, (x2, y2), 2, (255, 0, 0), cv2.FILLED)

                            cv2.circle(frame, (x3, y3), 2, (255, 0, 0), cv2.FILLED)
                            cv2.circle(frame, (x4, y4), 2, (255, 0, 0), cv2.FILLED)

                            faces = self.detector.process(frameRGB)

                            if faces.detections is not None:
                                print('detecta')
                                for face in faces.detections:
                                    score = face.score
                                    score = score[0]
                                    print(score)
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if score > confThreshold:
                                        # print('hola')
                                        xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, anc, alt = int(xi * an), int(yi * al), int(anc * an), int(alt * al)
                                        print(xi)
                                        print(yi)
                                        print(anc)
                                        print(alt)

                                        offsetan = (offsetx / 100) * anc
                                        xi = int(xi - int(offsetan / 2))
                                        anc = int(anc + offsetan)

                                        offsetal = (offsety / 100) * alt
                                        yi = int(yi - int(offsetal / 2))
                                        alt = int(alt + offsetal)
                                        cv2.rectangle(frame, (xi, yi, anc, alt), (255, 0, 255), 2)
                                        self.label_video.texture = self.texture
                                        #if xi < 0: xi = 0
                                       # if yi < 0: yi = 0
                                        #if anc < 0: anc = 0
                                        #if alt < 0: alt = 0



            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            self.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')

            self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.label_video.texture = self.texture

    def on_leave(self):
        self.capture.release()


confThreshold = 0.5

offsety = 30
offsetx = 20

class MedicalApp(App):
    def build(self):
        sm = ScreenManager()
        main_screen = MainScreen(name='main')
        camera_screen = CameraScreen(name='camera')
        sm.add_widget(main_screen)
        sm.add_widget(camera_screen)
        return sm


if __name__ == '__main__':
    MedicalApp().run()



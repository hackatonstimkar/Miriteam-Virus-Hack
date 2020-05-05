import threading
import time
import tkinter as tk

import speech_recognition as sr
from PIL import Image, ImageTk

import cv2 as cv
from app.ctx import (age_gender_recognition_net, emotion_recognition_net,
                     face_detection_net, head_pose_estimation_net, slide)
from app.Stream import Stream


class App:
    def __init__(self):
        self.active = False
        self.prev_active = self.active
        self.stream = Stream()

        self.setup_gui()

        self.buy_list = []
        self.buy_list_18 = ['пиво', 'вино', 'сигареты', "водка", "алгоголь", "коньяк", 'портвейн']
        self.display = slide[0]

        self.r = sr.Recognizer()
        self.micro = sr.Microphone(device_index=1)
        self.last_phrase = ''

        with self.micro as source:
            self.r.adjust_for_ambient_noise(source)

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Virus-hack Miriteam")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # GUI elements
        self.video = tk.Label(self.root, bd=0)
        self.slide = tk.Label(self.root, bd=0)
        self.text = tk.Label(self.root, bd=0)
        self.runtime = tk.Label(self.root, bd=0)

        # GUI element positions
        self.video.grid(row=0, column=0, rowspan=100, columnspan=2)
        self.slide.grid(row=0, column=3, rowspan=100, columnspan=2)
        self.text.grid(row=100, column=0, rowspan=1, columnspan=1)
        self.runtime.grid(row=100, column=1, rowspan=1, columnspan=1)

    def loop(self):
        frame = self.stream.get_frame()
        output_image = frame.copy()

        faces = face_detection_net.detect(frame, 0.6)
        face_detection_net.draw(output_image)

        self.active = True if len(faces) else False

        if self.active != self.prev_active:
            if self.active:
                threading.Thread(target=self.voice_recognition).start()

        self.prev_active = self.active

        for fxmin, fymin, fxmax, fymax in faces:
            face_region = (fxmin, fymin, fxmax, fymax)
            face_crop = frame[fymin:fymax, fxmin:fxmax]

            age_gender_recognition_net.detect(face_crop)
            age_gender_recognition_net.draw(output_image, face_region)

            emotion_recognition_net.detect(face_crop)
            emotion_recognition_net.draw(output_image, face_region)

            head_pose_estimation_net.detect(face_crop)
            head_pose_estimation_net.draw(output_image, face_region)

        self.runtime.configure(text=f"Runtime: {self.stream.runtime:.0f}s")
        self.text.configure(text=f"Last phrase: {self.last_phrase}")

        self.show_image(self.resize_image(output_image, 720), self.video)

        self.draw_buy_list(slide[1])
        self.show_image(self.resize_image(self.display, 720), self.slide)

        self.root.after(15, self.loop)

    def voice_recognition(self):
        with self.micro as source:
            while self.active:
                audio = self.r.listen(source, phrase_time_limit=3)

                try:
                    self.last_phrase = self.r.recognize_google(
                        audio, language="ru-RU").lower()

                    if 'начать' in self.last_phrase.split():
                        self.display = slide[1]

                    elif self.last_phrase.split()[0] in ['добавить', 'добавьте', 'хочу', 'желаю']:
                        self.buy_list.append(self.last_phrase.split()[-1])

                    elif self.last_phrase.split()[0] not in ['начать', 'завершить', 'удалить', 'убрать']:
                        self.buy_list.append(self.last_phrase.split()[-1])

                    elif self.last_phrase.split()[0] in ['удалить', 'убрать']:
                        self.buy_list.remove(self.last_phrase.split()[-1])

                    elif 'завершить' in self.last_phrase.split():
                        self.display = slide[2]
                        self.active = False
                        self.prev_active = False
                        time.sleep(5)
                        self.display = slide[0]
                        self.buy_list = []

                except Exception:
                    pass

    def reverse_active(self):
        self.active = not self.active
        self.button.configure(
            text="Начать" if not self.active else "Завершить")

        if self.active:
            threading.Thread(target=self.voice_recognition).start()

    def show_image(self, output_image, element):
        output_image = cv.cvtColor(output_image, cv.COLOR_BGR2RGBA)
        output_image = Image.fromarray(output_image)
        output_image = ImageTk.PhotoImage(output_image)

        element.configure(image=output_image)
        element.image = output_image

    def draw_buy_list(self, frame):
        y_pos = 120
        cv.rectangle(frame, (0, y_pos), frame.shape[:2], (255, 255, 255), -1)
        for x in self.buy_list:
            y_pos += 50
            if x in self.buy_list_18:
                x += '(!18+!)'
            cv.putText(frame, x, (10, y_pos), cv.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)

    def resize_image(self, image, h):
        scale = h / image.shape[0]
        dsize = (int(image.shape[1] * scale), (int(image.shape[0] * scale)))
        return cv.resize(image, dsize)

    def run(self):
        self.loop()
        self.root.mainloop()

    def on_closing(self):
        self.active = False
        self.root.destroy()

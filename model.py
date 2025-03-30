# model.py
from torchvision.models.quantization import googlenet
from ultralytics import YOLO
from translations import UKRAINIAN_TRANSLATIONS
import cv2
from gtts import gTTS
import os


class ImageRecognitionModel:
    def __init__(self):
        self.model = YOLO('yolov8l.pt')

    def speak(self, text, lang='uk', filename="outp55ut.mp3"):
        """
        Функція для озвучення тексту за допомогою gTTS.
        """
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        os.system(f"afplay {filename}")  # Для Windows, заміни на 'afplay' для macOS або 'mpg321' для Linux

    def detect_objects(self, image):
        results = self.model(image)
        detected_objects = {}

        for r in results:
            boxes = r.boxes

            for box in boxes:
                cls = int(box.cls[0])
                name = self.model.names[cls]
                ukr_name = UKRAINIAN_TRANSLATIONS.get(name.lower(), name)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                image = cv2.putText(image, ukr_name, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                detected_objects[ukr_name] = detected_objects.get(ukr_name, 0) + 1

        # Якщо знайдені об'єкти, озвучуємо їх
        if detected_objects:
            text_to_speak = "Об'єкти в кадрі: " + ", ".join(
                [f"{obj} ({count})" for obj, count in detected_objects.items()])
            self.speak(text_to_speak)

        return detected_objects, image
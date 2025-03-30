# gui.py
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from model import ImageRecognitionModel


class ImageRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Demooko")
        self.model = ImageRecognitionModel()
        self.video_capture = None
        self._init_ui()

    def _init_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.upload_btn = tk.Button(self.frame, text="Завантажити фото", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.video_btn = tk.Button(self.frame, text="Запустити відео", command=self.start_video)
        self.video_btn.pack(pady=5)

        self.canvas = tk.Canvas(self.frame, width=640, height=480)
        self.canvas.pack()

        self.result_text = tk.Text(self.frame, height=10, width=50)
        self.result_text.pack(pady=5)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            image = cv2.imread(file_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.process_frame(image_rgb)

    def start_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            self.video_capture = cv2.VideoCapture(file_path)
            self.process_video()

    def process_video(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.process_frame(frame_rgb)
            self.root.after(30, self.process_video)
        else:
            self.video_capture.release()

    def process_frame(self, frame):
        detected_objects, annotated_frame = self.model.detect_objects(frame)
        self.display_image(annotated_frame)
        self.display_results(detected_objects)

    def display_image(self, image):
        height, width = image.shape[:2]
        scale = min(640 / width, 480 / height)
        new_size = (int(width * scale), int(height * scale))
        image = cv2.resize(image, new_size)
        photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.canvas.create_image(320, 240, image=photo, anchor=tk.CENTER)
        self.canvas.image = photo

    def display_results(self, detected_objects):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Detected Objects:\n\n")
        for obj, count in detected_objects.items():
            self.result_text.insert(tk.END, f"{obj}: {count}\n")


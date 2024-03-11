import cv2
import mediapipe as mp
import threading
import time
import ctypes
import queue
# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DPI = 100  # Placeholder, assume appropriate DPI is provided
DPI_SENSITIVITY = 0.5  # Adjust based on personal preference

class VideoCapture:
    def __init__(self, queue):
        self.cap = cv2.VideoCapture(0)
        self.queue = queue
        self.running = True

    def run(self):
        while self.running:
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            image = cv2.flip(image, 1)
            self.queue.put(image)
            time.sleep(0.01)  # Adjust frame capture rate as needed

    def stop(self):
        self.running = False


class MeshProcessor:
    def __init__(self, queue, output_queue):
        import mediapipe as mp
        self.face_mesh = mp.solutions.face_mesh(
            max_num_faces=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.queue = queue
        self.output_queue = output_queue

    def run(self):
        with self.face_mesh as face_mesh:
            while True:
                image = self.queue.get()
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image_rgb)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        nose_x, nose_y = 0, 0
                        for landmark in face_landmarks.landmark:
                            temp = []
                            temp.append(landmark.x)
                            if len(temp)==2:
                                nose_x = int(landmark.x * image.shape[1])
                                nose_y = int(landmark.y * image.shape[0])
                                break
                        mouse_x = int(nose_x * SCREEN_WIDTH * DPI_SENSITIVITY / DPI)
                        mouse_y = int(nose_y * SCREEN_HEIGHT * DPI_SENSITIVITY / DPI)
                        self.output_queue.put((mouse_x, mouse_y))

    def close(self):
        self.face_mesh.close()


class MouseMover:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        while True:
            x, y = self.queue.get()
            ctypes.windll.user32.SetCursorPos((x, y))


# Create and run threads
capture_queue = queue.Queue()
process_queue = queue.Queue()
output_queue = queue.Queue()

capture_thread = threading.Thread(target=VideoCapture(capture_queue).run)
process_thread = threading.Thread(target=MeshProcessor(process_queue, output_queue).run)
move_thread = threading.Thread(target=MouseMover(output_queue).run)

capture_thread.start()
process_thread.start()
move_thread.start()

# Keyboard input and thread termination
import keyboard as kb
while True:
    if kb.is_pressed('esc'):
        capture_thread.join()
        process_thread.join()
        move_thread.join()
        break

# Resource management
mp.solutions.face_mesh.close()
cv2.destroyAllWindows()

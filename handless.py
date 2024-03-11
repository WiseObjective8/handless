import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import pyautogui as pa
import mouse
import ctypes

plt.ion()
w, h = pa.size()
mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
cap = cv2.VideoCapture(0)
fig, ax = plt.subplots()
px = py = 0
sense = 0.4
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    ax.clear()  # Clear the previous plot once per iteration
    plt.gca().invert_yaxis()

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            x_val = []
            y_val = []
            x_s = []
            y_s = []
            for landmark in face_landmarks.landmark:
                x_val.append(landmark.x)
                y_val.append(landmark.y)
                if len(x_val) == 2:
                    nose_x, nose_y = int(landmark.x * w), int(landmark.y * h)
                    x, y = int(px*(1-sense)+nose_x*sense), int(py *
                                                               (1-sense)+nose_y*sense)
                    ctypes.windll.user32.SetCursorPos(x, y)
                    x_s.append(landmark.x)
                    y_s.append(landmark.y)
                    px, py = x, y
            plt.scatter(x_val, y_val)
            plt.scatter(x_s, y_s)
    import keyboard as kb
    if cv2.waitKey(1) & 0xFF == 27 or kb.is_pressed('space'):
        plt.clf()
        plt.cla()
        plt.close()
        break

plt.ioff()
plt.show()
plt.close('all')
cap.release()
cv2.destroyAllWindows()

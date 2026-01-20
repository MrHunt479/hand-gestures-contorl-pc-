import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def perform_action(action):
    if action == "click":
        pyautogui.click()
    elif action == "swipe_left":
        pyautogui.hotkey('alt', 'left')
    elif action == "swipe_right":
        pyautogui.hotkey('alt', 'right')
    elif action == "scroll_up":
        pyautogui.scroll(100)
    elif action == "scroll_down":
        pyautogui.scroll(-100)
    elif action == "zoom_in":
        pyautogui.hotkey('ctrl', '+')
    elif action == "zoom_out":
        pyautogui.hotkey('ctrl', '-')

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of thumb and index finger
            thumb_tip = (landmarks.landmark[4].x, landmarks.landmark[4].y)
            index_tip = (landmarks.landmark[8].x, landmarks.landmark[8].y)
            distance = calculate_distance(thumb_tip, index_tip)

            # Example: Click when thumb and index finger are close
            if distance < 0.05:
                perform_action("click")
                cv2.putText(frame, "Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Example: Swipe left when index finger moves left
            if index_tip[0] < 0.3:
                perform_action("swipe_left")
                cv2.putText(frame, "Swipe Left", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Example: Swipe right when index finger moves right
            if index_tip[0] > 0.7:
                perform_action("swipe_right")
                cv2.putText(frame, "Swipe Right", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Example: Scroll up when hand moves up
            if index_tip[1] < 0.3:
                perform_action("scroll_up")
                cv2.putText(frame, "Scroll Up", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Example: Scroll down when hand moves down
            if index_tip[1] > 0.7:
                perform_action("scroll_down")
                cv2.putText(frame, "Scroll Down", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Example: Zoom in when thumb and index finger form a circle
            if distance < 0.03:
                perform_action("zoom_in")
                cv2.putText(frame, "Zoom In", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Gesture Control', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

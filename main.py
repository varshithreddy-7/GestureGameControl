import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

MODE_MENU = "MENU"
MODE_GAME = "GAME"
mode = MODE_MENU

click_cooldown = 1
last_click_time = 0

screen_w, screen_h = pyautogui.size()
prev_x, prev_y = 0, 0
smoothening = 5

def fingers_up(hand_landmarks):
    fingers = []
    tips_ids = [4, 8, 12, 16, 20]

    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)  # Thumb
    else:
        fingers.append(0)

    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    h, w, _ = img.shape

    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            lm_list = hand_landmark.landmark
            mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)
            fingers = fingers_up(hand_landmark)
            total_fingers = sum(fingers)

            # Switch between menu and game modes
            if total_fingers == 5:
                mode = MODE_MENU
            elif fingers[1] == 1 and total_fingers == 1:
                mode = MODE_GAME

            if mode == MODE_MENU:
                cv2.putText(img, "Mode: MENU", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Move cursor with index finger
                x1 = int(lm_list[8].x * w)
                y1 = int(lm_list[8].y * h)
                screen_x = np.interp(x1, [0, w], [0, screen_w])
                screen_y = np.interp(y1, [0, h], [0, screen_h])
                cur_x = prev_x + (screen_x - prev_x) / smoothening
                cur_y = prev_y + (screen_y - prev_y) / smoothening
                pyautogui.moveTo(cur_x, cur_y)
                prev_x, prev_y = cur_x, cur_y

                # Tap gesture = index + thumb close together
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                distance = ((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2) ** 0.5
                if distance < 0.05:
                    if time.time() - last_click_time > click_cooldown:
                        pyautogui.click()
                        last_click_time = time.time()

            elif mode == MODE_GAME:
                cv2.putText(img, "Mode: GAME", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Drive forward (thumb up only)
                if fingers[0] == 1 and sum(fingers) == 1:
                    pyautogui.keyDown("right")
                else:
                    pyautogui.keyUp("right")

                # Drive backward (index up only)
                if fingers[1] == 1 and sum(fingers) == 1:
                    pyautogui.keyDown("left")
                else:
                    pyautogui.keyUp("left")

                # Brake or reverse (fist = no fingers up)
                if sum(fingers) == 0:
                    pyautogui.keyDown("down")
                else:
                    pyautogui.keyUp("down")

    else:
        # Reset all key presses if hand is not visible
        pyautogui.keyUp("right")
        pyautogui.keyUp("left")
        pyautogui.keyUp("down")

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

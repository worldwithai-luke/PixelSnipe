import cv2
import numpy as np
import threading
import time
import win32api
import pyautogui

from capture import Capture
from mouse import ArduinoMouse
from fov_window import show_detection_window, toggle_window


class Pixelsnipe:
    # HSV color range for detection (you can tweak this)
    LOWER_COLOR = np.array([141, 98, 169])
    UPPER_COLOR = np.array([171, 194, 255])
    DEADZONE = 2
    TARGET_SWITCH_DELAY = 0.1  # 0.1-second delay when switching targets

    def __init__(self, x, y, xfov, yfov, FLICKSPEED, MOVESPEED, RECOIL_SPEED=0.164):
        self.arduinomouse = ArduinoMouse()
        self.grabber = Capture(x, y, xfov, yfov)
        self.flickspeed = FLICKSPEED
        self.movespeed = MOVESPEED
        self.recoil_speed = RECOIL_SPEED
        self.toggled = False
        self.window_toggled = False
        self.tracking = False  # Track only when actively following target
        self.last_target = None
        self.last_seen_time = 0
        self.last_target_switch_time = 0  # Time of last target switch
        self.shooting = False
        threading.Thread(target=self.track_target, daemon=True).start()
        threading.Thread(target=self.listen, daemon=True).start()

    def toggle(self):
        self.toggled = not self.toggled
        time.sleep(0.2)

    def close(self):
        # Placeholder for cleanup if needed (e.g., closing windows or releasing resources)
        pass

    def listen(self):
        while True:
            if win32api.GetAsyncKeyState(0x71) < 0:  # F2 to toggle display window
                toggle_window(self)
                time.sleep(0.2)

            right_click = win32api.GetAsyncKeyState(0x02) < 0  # Right mouse
            alt_key = win32api.GetAsyncKeyState(0x12) < 0      # Alt key
            left_click = win32api.GetAsyncKeyState(0x01) < 0   # Left mouse for recoil

            if self.toggled:
                if right_click:
                    self.tracking = True
                    self.process("move")
                elif alt_key:
                    self.tracking = True
                    self.process("click")
                else:
                    self.tracking = False
                self.shooting = left_click  # Update shooting state for recoil
            else:
                self.tracking = False
                self.shooting = False

            time.sleep(0.005)  # Minimal sleep to prevent CPU overuse

    def process(self, action):
        # Capture screen and preprocess once
        screen = self.grabber.get_screen()
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_COLOR, self.UPPER_COLOR)
        dilated = cv2.dilate(mask, None, iterations=5)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            self.last_target = None
            return

        # Center of the capture area
        center_x = self.grabber.xfov // 2
        center_y = self.grabber.yfov // 2
        closest_contour = None
        min_distance = float('inf')
        min_area_threshold = 100  # Filter smaller noise

        for contour in contours:
            # Filter small contours
            area = cv2.contourArea(contour)
            if area < min_area_threshold:
                continue

            # Calculate centroid using moments
            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            contour_center = (cX, cY)

            # Calculate Euclidean distance from contour center to capture center
            distance = np.sqrt((contour_center[0] - center_x) ** 2 + (contour_center[1] - center_y) ** 2)

            # Weight distance by contour area to prioritize larger, closer contours
            weighted_distance = distance / (area ** 0.3)

            if weighted_distance < min_distance:
                min_distance = weighted_distance
                closest_contour = contour

        if closest_contour is None:
            self.last_target = None
            return

        # Check if switching to a new target
        current_time = time.time()
        if closest_contour is not self.last_target and current_time - self.last_target_switch_time < self.TARGET_SWITCH_DELAY:
            # Stick with the last target if within 0.1 seconds
            if self.last_target is None:
                self.last_target = closest_contour
                self.last_target_switch_time = current_time
            else:
                closest_contour = self.last_target
        else:
            # Update to new target
            self.last_target = closest_contour
            self.last_target_switch_time = current_time

        # Process the selected contour
        M = cv2.moments(closest_contour)
        if M["m00"] == 0:
            self.last_target = None
            return
        cX = int(M["m10"] / M["m00"])

        # Get bounding rect for headshot aiming
        x, y, w, h = cv2.boundingRect(closest_contour)
        y_offset = int(h * 0.18)  # Aim ~17.5% from top (headshot)

        # Update last seen time
        self.last_seen_time = current_time

        if action == "move":
            target_x = cX  # Use centroid x for horizontal aiming
            target_y = y + y_offset  # Use top of bounding rect + offset for headshot
            x_diff = target_x - self.grabber.xfov // 2
            y_diff = target_y - self.grabber.yfov // 2

            # Only move if outside deadzone to avoid jitter
            if abs(x_diff) > self.DEADZONE or abs(y_diff) > self.DEADZONE:
                move_x = np.clip(x_diff * self.movespeed * 2.24, -20, 20)
                move_y = np.clip(y_diff * self.movespeed * 2.24, -20, 20)
                self.arduinomouse.move(move_x, move_y)

            # Apply recoil compensation if shooting
            if self.shooting:
                self.arduinomouse.move(0, self.recoil_speed)

        elif action == "click":
            # Only click if target's head is near center
            if abs(cX - self.grabber.xfov // 2) <= 4 and abs(y + y_offset - self.grabber.yfov // 2) <= 10:
                self.arduinomouse.click()

    def track_target(self):
        while True:
            if self.tracking:
                self.process("move")  # Call process with "move" action
            time.sleep(0.0001)  # Reduced sleep for faster tracking
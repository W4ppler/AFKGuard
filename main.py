import math
import random
import sys
import pyautogui
import pydirectinput
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSystemTrayIcon, QMenu, QGridLayout, QFrame, QLineEdit, QLabel, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from pynput import keyboard


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AFKGuard")
        self.setGeometry(100, 100, 380, 160)

        # Sets the window to always be in front
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # The program cannot be fully closed with the X, but with the tray menu
        #self.setAttribute(Qt.WA_QuitOnClose, False)
        #self.create_tray_icon()

        # Create a QVBoxLayout to arrange buttons vertically
        self.layout = QGridLayout()


        # Move Mouse - Button
        self.buttonMoveMouse = QPushButton("Move Mouse (F5)", self)
        self.buttonMoveMouse.clicked.connect(self.startMovingMouse)
        # Move Mouse - Input
        self.inputMoveMouse = QLineEdit(self)
        self.inputMoveMouse.setPlaceholderText("1")
        # Move Mouse - Labels
        self.labelMoveMouse = QLabel("Scale: ", self)
        # Adding them to the layout
        self.layout.addWidget(self.buttonMoveMouse, 0, 0)
        self.layout.addWidget(self.labelMoveMouse, 0, 1)
        self.layout.addWidget(self.inputMoveMouse, 0, 2, 1, 3)


        # Press Keys - Button
        self.buttonPressKeys = QPushButton("Press Keys (F6)", self)
        self.buttonPressKeys.clicked.connect(self.startPressingKeys)
        # Press Keys - Input
        self.inputPressKeys = QLineEdit(self)
        self.inputPressKeys.setPlaceholderText("w;a;s;d")
        # Press Keys - Labels
        self.labelPressKeys = QLabel("Keys: ", self)
        # Adding them to the layout
        self.layout.addWidget(self.buttonPressKeys, 1, 0)
        self.layout.addWidget(self.labelPressKeys, 1, 1)
        self.layout.addWidget(self.inputPressKeys, 1, 2, 1, 3)


        # Click - Button
        self.buttonClick = QPushButton("Click (F7)", self)
        self.buttonClick.clicked.connect(self.startClicking)
        # Click - Input
        self.inputClick = QLineEdit(self)
        self.inputClick.setPlaceholderText("1")
        # Click - Labels
        self.labelClick = QLabel("Clicks/s: ", self)
        # Adding them to the layout
        self.layout.addWidget(self.buttonClick, 3, 0)
        self.layout.addWidget(self.labelClick, 3, 1)
        self.layout.addWidget(self.inputClick, 3, 2, 1, 3)


        # Stop Button
        self.buttonStop = QPushButton("stop (F8)", self)
        self.buttonStop.clicked.connect(self.stop)
        # Adding it to the layout
        self.layout.addWidget(self.buttonStop, 5, 0)


        # Duration Label
        self.labelDuration = QLabel("Duration: ", self)
        self.labelDurationHint = QLabel("(empty => until stopped)", self)
        # Duration input
        self.inputDurationHours = QLineEdit(self)
        self.inputDurationHours.setPlaceholderText("Hours")
        self.labelDurationMinutes = QLineEdit(self)
        self.labelDurationMinutes.setPlaceholderText("Minutes")
        self.labelDurationSeconds = QLineEdit(self)
        self.labelDurationSeconds.setPlaceholderText("Seconds")
        # Adding to layout
        self.layout.addWidget(self.labelDuration, 5, 1)
        self.layout.addWidget(self.labelDurationHint, 6, 2, 1, 3)
        self.layout.addWidget(self.inputDurationHours, 5, 2)
        self.layout.addWidget(self.labelDurationMinutes, 5, 3)
        self.layout.addWidget(self.labelDurationSeconds, 5, 4)


        # Seperator line
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.HLine)
        # Adding to the layout
        self.layout.addWidget(self.h_line, 4, 0, 1, 5)


        # Set the layout for the window
        self.setLayout(self.layout)

        # Initialize stop flag and timers
        self.stopped = False
        self.timerMoveMouse = QTimer(self)
        self.timerMoveMouse.timeout.connect(self.moveMouse)

        self.timerPressKeys = QTimer(self)
        self.timerPressKeys.timeout.connect(self.pressKeys)

        self.timerClick = QTimer(self)
        self.timerClick.timeout.connect(self.click)

        self.timerStop = QTimer(self)
        self.timerStop.timeout.connect(self.stop)

        # Screen size
        self.width, self.height = pyautogui.size()

        # Start listening for keyboard inputs
        self.listener = keyboard.Listener(on_press=self.keyPressed)
        self.listener.start()

    def create_tray_icon(self):
        icon = QIcon("icon.png")  # Load your PNG icon
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.show()


    def keyPressed(self, key):
        if key == keyboard.Key.f5:
            self.buttonMoveMouse.animateClick()
            self.buttonMoveMouse.click()
        if key == keyboard.Key.f6:
            self.buttonPressKeys.animateClick()
            self.buttonPressKeys.click()
        if key == keyboard.Key.f7:
            self.buttonClick.animateClick()
            self.buttonClick.click()
        if key == keyboard.Key.f8:
            self.buttonStop.animateClick()
            self.buttonStop.click()

    def startMovingMouse(self):
        self.stopped = False

        # Get scale value from input field
        scale = self.inputMoveMouse.text()
        try:
            scale = int(scale)
        except ValueError:
            print("Invalid scale value, using default (1)")
            scale = 1

        if self.timerMoveMouse.isActive():
            print(f"Timer already running, not setting a new one")
        else:
            durationHours = self.inputDurationHours.text()
            durationMinutes = self.labelDurationMinutes.text()
            durationSeconds = self.labelDurationSeconds.text()

            try:
                durationHours = int(durationHours)
            except ValueError:
                durationHours = 0

            try:
                durationMinutes = int(durationMinutes)
            except ValueError:
                durationMinutes = 0

            try:
                durationSeconds = int(durationSeconds)
            except ValueError:
                durationSeconds = 0


            if(durationHours == 0 and durationMinutes == 0 and durationSeconds == 0):
                print("Duration: until stopped")
            else:
                duration = durationHours * 3600 + durationMinutes * 60 + durationSeconds
                duration *= 1000
                print(f"Duration: {durationHours} hour(s) {durationMinutes} minute(s) {durationSeconds} second(s) (={duration}ms)")
                self.timerStop.start(duration)

        print(f"Moving mouse with scale: {scale}")

        self.timerMoveMouse.start(int(100/scale))

    def moveMouse(self):
        if self.stopped:
            self.timerMoveMouse.stop()
            return

        scale = self.inputMoveMouse.text()
        try:
            scale = int(scale)
            if scale < 0:
                raise ValueError()
        except ValueError:
            scale = 1

        scale += 50

        x = random.randint(-10 * scale, 10 * scale)
        y = random.randint(-10 * scale, 10 * scale)

        num_steps = 10
        for i in range(num_steps):
            x = x * (i + 1) / num_steps
            y = y * (i + 1) / num_steps

            current_x, current_y = pyautogui.position()
            target_x = current_x + x
            target_y = current_y + y

            if target_x < 10 or target_y < 10:
                pydirectinput.move(int(self.width/2), int(self.height/2))

            pydirectinput.moveRel(int(x), int(y))


        # Ensure the mouse doesn't get stuck in a corner by making small random movements
        pydirectinput.moveRel(random.randint(-1, 1), random.randint(-1, 1))
                    

    def startPressingKeys(self):
        self.stopped = False

        if self.timerMoveMouse.isActive():
            print(f"Timer already running, not setting a new one")
        else:
            durationHours = self.inputDurationHours.text()
            durationMinutes = self.labelDurationMinutes.text()
            durationSeconds = self.labelDurationSeconds.text()

            try:
                durationHours = int(durationHours)
            except ValueError:
                durationHours = 0

            try:
                durationMinutes = int(durationMinutes)
            except ValueError:
                durationMinutes = 0

            try:
                durationSeconds = int(durationSeconds)
            except ValueError:
                durationSeconds = 0

            if (durationHours == 0 and durationMinutes == 0 and durationSeconds == 0):
                print("Duration: until stopped")
            else:
                duration = durationHours * 3600 + durationMinutes * 60 + durationSeconds
                duration *= 1000
                print(
                    f"Duration: {durationHours} hour(s) {durationMinutes} minute(s) {durationSeconds} second(s) (={duration}ms)")
                self.timerStop.start(duration)

        # Get Keys value from input field
        keyString = self.inputPressKeys.text()
        self.keys = list()

        for i in range(len(keyString)):
            if i%2==0:
                self.keys.append(keyString[i])

        if len(self.keys)==0:
            self.keys.append("w")
            self.keys.append("a")
            self.keys.append("s")
            self.keys.append("d")

        print(f"Pressing the following keys: {self.keys}")

        self.timerPressKeys.start(1000)

    def pressKeys(self):
        if self.stopped:
            self.timerPressKeys.stop()

        i = math.floor(random.random()*len(self.keys))

        key = self.keys[i]

        pydirectinput.keyDown(key)
        time.sleep(1)
        pydirectinput.keyUp(key)

    def startClicking(self):
        self.stopped = False

        if self.timerMoveMouse.isActive():
            print(f"Timer already running, not setting a new one")
        else:
            durationHours = self.inputDurationHours.text()
            durationMinutes = self.labelDurationMinutes.text()
            durationSeconds = self.labelDurationSeconds.text()

            try:
                durationHours = int(durationHours)
            except ValueError:
                durationHours = 0

            try:
                durationMinutes = int(durationMinutes)
            except ValueError:
                durationMinutes = 0

            try:
                durationSeconds = int(durationSeconds)
            except ValueError:
                durationSeconds = 0

            if (durationHours == 0 and durationMinutes == 0 and durationSeconds == 0):
                print("Duration: until stopped")
            else:
                duration = durationHours * 3600 + durationMinutes * 60 + durationSeconds
                duration *= 1000
                print(
                    f"Duration: {durationHours} hour(s) {durationMinutes} minute(s) {durationSeconds} second(s) (={duration}ms)")
                self.timerStop.start(duration)

        # Get clicks value from input field
        clicks = self.inputClick.text()
        try:
            clicks = int(clicks)
            if clicks<0:
                raise ValueError()
        except ValueError:
            print("Invalid Clickspeed value, using default (1)")
            clicks = 1

        print(f"Clicking with speed: {clicks}")

        # Default Value is 1s (1000ms)
        clicks=int(1000/clicks)
        self.timerClick.start(clicks)

    def click(self):
        if self.stopped:
            self.timerClick.stop()
        else:
            pydirectinput.click()

    def stop(self):
        print("Stopping actions.")
        self.stopped = True
        self.timerStop.stop()

# Create the application object
app = QApplication(sys.argv)

# Create and show the window
window = MyWindow()
window.show()

# Start the application event loop
sys.exit(app.exec_())

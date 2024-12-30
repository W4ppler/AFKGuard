import math
import random
import sys
import pyautogui
import pydirectinput
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QFrame, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QTimer
from pynput import keyboard


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AFKGuard")
        self.setGeometry(100, 100, 300, 200)

        # Sets the window to always be in front
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Create a QVBoxLayout to arrange buttons vertically
        self.layout = QGridLayout()

        # Create buttons
        self.buttonMoveMouse = QPushButton("Move Mouse until stopped", self)
        self.buttonPressKeys = QPushButton("Press Keys until stopped", self)
        self.buttonClick = QPushButton("Click until stopped", self)
        self.buttonStop = QPushButton("stop (F6)", self)

        # Create the input fields
        self.inputMoveMouse = QLineEdit(self)
        self.inputMoveMouse.setPlaceholderText("1")
        self.inputClick = QLineEdit(self)
        self.inputClick.setPlaceholderText("1")

        # Create labels
        self.labelMoveMouse = QLabel("    Scale: ", self)
        self.labelClick = QLabel("    Speed: ", self)

        # Create seperator line
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.HLine)

        # Add Widgets to the layout
        self.layout.addWidget(self.buttonMoveMouse, 0, 0)
        self.layout.addWidget(self.labelMoveMouse, 0, 1)
        self.layout.addWidget(self.inputMoveMouse, 0, 2)
        self.layout.addWidget(self.buttonPressKeys, 1, 0)
        self.layout.addWidget(self.buttonClick, 3, 0)
        self.layout.addWidget(self.labelClick, 3, 1)
        self.layout.addWidget(self.inputClick, 3, 2)
        self.layout.addWidget(self.h_line, 4, 0, 1, 5)
        self.layout.addWidget(self.buttonStop, 5, 0)

        # Connect buttons to their respective slots
        self.buttonMoveMouse.clicked.connect(self.startMovingMouse)
        self.buttonPressKeys.clicked.connect(self.startPressingKeys)
        self.buttonClick.clicked.connect(self.startClicking)
        self.buttonStop.clicked.connect(self.stop)

        # Set the layout for the window
        self.setLayout(self.layout)

        # Initialize stopped flag and timers
        self.stopped = False
        self.timerMoveMouse = QTimer(self)
        self.timerMoveMouse.timeout.connect(self.moveMouse)

        self.timerPressKeys = QTimer(self)
        self.timerPressKeys.timeout.connect(self.pressKeys)

        self.timerClick = QTimer(self)
        self.timerClick.timeout.connect(self.click)

        # Screen size
        self.width, self.height = pyautogui.size()

        # Start listening for keyboard inputs
        self.listener = keyboard.Listener(on_press=self.keyPressed)
        self.listener.start()

    def keyPressed(self, key):
        try:
            if key == keyboard.Key.f6:
                self.buttonStop.animateClick()
                self.stop()
        except AttributeError:
            pass


    def startMovingMouse(self):
        self.stopped = False

        # Get scale value from input field
        scale = self.inputMoveMouse.text()
        try:
            scale = int(scale)
        except ValueError:
            print("Invalid scale value, using default (1)")
            scale = 1

        print(f"Moving mouse with scale: {scale}")
        self.timerMoveMouse.start(500)

    def moveMouse(self):
        if self.stopped:
            self.timerMoveMouse.stop()
        else:
            # Get scale value from input field for mouse movement
            scale = self.inputMoveMouse.text()
            try:
                scale = int(scale)
                if scale<1:
                    scale=1
            except ValueError:
                scale = 1  # default scale value

            pydirectinput.moveRel(scale,0)
            pydirectinput.moveRel(-scale,0)

    def startPressingKeys(self):
        self.stopped = False
        print("Pressing keys.")
        self.timerPressKeys.start(1000)

    def pressKeys(self):
        if self.stopped:
            self.timerPressKeys.stop()
        else:
            key=math.floor(random.random()*4)
            if key == 0:
                pydirectinput.keyDown('w')
                time.sleep(1)
                pydirectinput.keyUp('w')
            elif key == 1:
                pydirectinput.keyDown('a')
                time.sleep(1)
                pydirectinput.keyUp('a')
            elif key == 2:
                pydirectinput.keyDown('s')
                time.sleep(1)
                pydirectinput.keyUp('s')
            else:
                pydirectinput.keyDown('d')
                time.sleep(1)
                pydirectinput.keyUp('d')

    def startClicking(self):
        self.stopped = False

        # Get scale value from input field
        speed = self.inputClick.text()
        try:
            speed = int(speed)
            if speed<1:
                speed=1
        except ValueError:
            print("Invalid scale value, using default (1)")
            speed = 1

        print(f"Clicking with speed: {speed}")

        # Default Value is 1s (1000ms)
        speed=int(1000/speed)
        self.timerClick.start(speed)

    def click(self):
        if self.stopped:
            self.timerClick.stop()
        else:

            pydirectinput.click()

    def stop(self):
        print("Stopping actions.")
        self.stopped = True

# Create the application object
app = QApplication(sys.argv)

# Create and show the window
window = MyWindow()
window.show()

# Start the application event loop
sys.exit(app.exec_())
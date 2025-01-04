import math
import random
import sys
import pyautogui
import pydirectinput
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFrame, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QTimer
from pynput import keyboard


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AFKGuard")
        self.setGeometry(100, 100, 350, 200)

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
        self.inputPressKeys = QLineEdit(self)
        self.inputPressKeys.setPlaceholderText("w;a;s;d")
        self.inputClick = QLineEdit(self)
        self.inputClick.setPlaceholderText("1")

        # Create labels
        self.labelMoveMouse = QLabel("    Scale: ", self)
        self.labelClick = QLabel("    Clicks/s: ", self)
        self.labelPressKeys = QLabel("    Keys: ", self)

        # Create seperator line
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.HLine)

        # Add Widgets to the layout
        self.layout.addWidget(self.buttonMoveMouse, 0, 0)
        self.layout.addWidget(self.labelMoveMouse, 0, 1)
        self.layout.addWidget(self.inputMoveMouse, 0, 2)
        self.layout.addWidget(self.buttonPressKeys, 1, 0)
        self.layout.addWidget(self.labelPressKeys, 1, 1)
        self.layout.addWidget(self.inputPressKeys, 1, 2)
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

        if scale==1:
            self.timerMoveMouse.start(250)


    def moveMouse(self):
        if self.stopped:
            self.timerMoveMouse.stop()
        else:
            # Get scale value from input field for mouse movement
            scale = self.inputMoveMouse.text()
            try:
                scale = int(scale)
                if scale<0:
                    raise ValueError()
            except ValueError:
                scale = 1  # default scale value

            pydirectinput.moveRel(scale,0)
            pydirectinput.moveRel(-scale,0)

                    

    def startPressingKeys(self):
        self.stopped = False

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

# Create the application object
app = QApplication(sys.argv)

# Create and show the window
window = MyWindow()
window.show()

# Start the application event loop
sys.exit(app.exec_())
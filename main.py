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
        self.setGeometry(100, 100, 350, 200)

        # Sets the window to always be in front
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


        #self.setAttribute(Qt.WA_QuitOnClose, False)
        #self.create_tray_icon()


        #self.setAttribute(Qt.WA_QuitOnClose, False)
        #self.create_tray_icon()
        #self.hide()

        # Create a QVBoxLayout to arrange buttons vertically
        self.layout = QGridLayout()

        # Create buttons
        self.buttonMoveMouse = QPushButton("Move Mouse until stopped (F5)", self)
        self.buttonPressKeys = QPushButton("Press Keys until stopped (F6)", self)
        self.buttonClick = QPushButton("Click until stopped (F7)", self)
        self.buttonStop = QPushButton("stop (F8)", self)

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

    def create_tray_icon(self):
        icon = QIcon("icon.png")  # Load your PNG icon
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.show()


    def closeEvent(self, event):
        # Hide the window instead of closing it
        self.hide()

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
            pydirectinput.moveRel(int(x), int(y))
            time.sleep(0.01)  # Small delay for smoothness

        # Ensure the mouse doesn't get stuck in a corner by making small random movements
        pydirectinput.moveRel(random.randint(-1, 1), random.randint(-1, 1))
                    

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

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

# Define the window class
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("QPushButton Example")
        self.setGeometry(100, 100, 300, 200)

        # Create the button
        self.button = QPushButton("Click Me!", self)

        # Connect the button click event to the slot (function)
        self.button.clicked.connect(self.on_button_click)

        # Resize the button to fit the text
        self.button.resize(self.button.sizeHint())

        # Move the button within the window
        self.button.move(100, 70)

    def on_button_click(self):
        print("Button clicked!")

# Create the application object
app = QApplication(sys.argv)

# Create the window
window = MyWindow()

# Show the window
window.show()

# Start the event loop
sys.exit(app.exec_())

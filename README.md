# AFKGuard

AFKGuard is designed to prevent you from going idle by simulating user activity. It can move the mouse, press keys, 
and click at regular intervals.

## Features

- **Move Mouse:** Moves the mouse back and forth until stopped.
- **Press Keys:** Randomly presses the 'W', 'A', 'S', and 'D' keys until stopped.
- **Click:** Simulates mouse clicks at a specified interval until stopped.
- **Stop Actions:** Stops all ongoing actions with a button click or by pressing the F6 key.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/W4ppler/AFKGuard.git
    cd afkguard
    ```

2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**
    ```bash
    ./main.exe
    ```

2. **Using the application:**
    - **Move Mouse:** Enter the scale value (default is 1) and click the "Move Mouse until stopped" button.
    - **Press Keys:** Click the "Press Keys until stopped" button to start pressing w,a,s and d.
    - **Click:** Enter the speed value (default is 1 click per second) and click the "Click until stopped" button.
    - **Stop Actions:** Click the "stop" button or press the F6 key to stop all actions.

## Dependencies

- Python 3.12.6
- PyQt5
- pyautogui
- pydirectinput
- pynput

## License

This project is licensed under the MIT License.

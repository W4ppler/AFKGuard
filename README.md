# AFKGuard

I have created AFKGuard, because I have searched for such a program a long time now. I have often found some programs but 
they never seemed work with games, because they would always use high level APIs (that's the reason why I use pydirectinput 
instead of pyautogui, which would be much easier to implement).

## Requirements
This program is designed for Windows operating systems only.

## Features

- **FAILSAFE MECHANISM** Moving the cursor to the top left corner causes the program to crash
- **Move Mouse:** Moves the mouse back and forth until stopped.
- **Press Keys:** Randomly presses the specified keys (standard is W,A,S,D) until stopped.
- **Click:** Simulates mouse clicks at a specified speed until stopped.
- **Stop Actions:** Stops all ongoing actions with a button click or by pressing the F6 key.
- **(NEW) Duration:** You can now set the duration of the guarding

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/W4ppler/AFKGuard.git
    cd afkguard
    ```

## Usage

1. **Run the application:**
    ```bash
    ./main.exe
    ```

2. **Using the application:**
    - **Move Mouse:** Enter the scale value (default is 1) and click the "Move Mouse until stopped" button.
    - **Press Keys:** Click the "Press Keys until stopped" button to start pressing w,a,s and d.
    - **Click:** Enter the speed value (default is 1 click per second) and click the "Click" button.
    - **Stop Actions:** Click the "stop" button or press the F6 key to stop all actions.


## Dependencies

- Python 3.12.6
- PyQt5
- pyautogui
- pydirectinput
- pynput

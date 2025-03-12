# Auto Clicker Tool

This project is an auto clicker tool implemented in Python. It allows users to simulate random key presses using a graphical user interface (GUI) built with Tkinter. The tool can run multiple threads to perform key presses at a specified rate.

## Files

- `src/autoClicker_cat.py`: Contains the main implementation of the auto clicker tool, including functions for random key presses, thread management, and GUI setup. It also includes logging functionality to display messages in a scrolled text widget.

- `requirements.txt`: Lists the dependencies required for the project.

## Requirements

To run this project, you need to install the following Python packages:

- `pydirectinput`
- `keyboard`
- `tkinter`

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Run the application by executing the `autoClicker_cat.py` script.
2. Enter the number of threads you want to run in the "Number of Threads" field.
3. Specify the run time in seconds in the "Run Time (seconds)" field. Enter `0` for infinite run time.
4. Click the "Start" button to begin the key pressing.
5. Click the "Stop" button to stop the key presses.
6. The log viewer will display the total number of key presses after stopping.

## Notes

- Ensure that the application has focus when running to simulate key presses effectively.
- Use responsibly and avoid using the tool in applications where it may violate terms of service.
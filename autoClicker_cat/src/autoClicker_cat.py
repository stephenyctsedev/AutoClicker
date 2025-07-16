import logging

# Configure logging to include timestamp
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from time import sleep, time
import random
import pydirectinput
import threading
import keyboard
import mouse
import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import StringVar

stop_threads = False
key_press_count = 0
start_run_time = 0
lock = threading.Lock()

root = tk.Tk()
root.title("Auto Clicker")

# Create a Tab Control
tab_control = ttk.Notebook(root)

# Create a tab for the auto clicker
auto_clicker_tab = ttk.Frame(tab_control)
tab_control.add(auto_clicker_tab, text='Random Key Presses')

# Create another tab for future use
new_tab = ttk.Frame(tab_control)
tab_control.add(new_tab, text='Mouse Position Clicker')

tab_control.pack(expand=1, fill="both")

run_time_var = StringVar()

# --- Mouse Position Clicker Tab ---

# Mouse position
tk.Label(new_tab, text="Mouse X:").grid(row=0, column=0, padx=5, pady=5)
mouse_x_entry = tk.Entry(new_tab)
mouse_x_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(new_tab, text="Mouse Y:").grid(row=0, column=2, padx=5, pady=5)
mouse_y_entry = tk.Entry(new_tab)
mouse_y_entry.grid(row=0, column=3, padx=5, pady=5)

get_mouse_pos_var = tk.BooleanVar(value=False)
get_mouse_pos_button = tk.Button(new_tab, text="Get Mouse Position")
get_mouse_pos_button.grid(row=1, column=0, columnspan=4, pady=10)

# Click interval
tk.Label(new_tab, text="Click Interval (sec):").grid(row=2, column=0, padx=5, pady=5)
interval_entry = tk.Entry(new_tab)
interval_entry.grid(row=2, column=1, padx=5, pady=5)
interval_entry.insert(0, "1")

# Start/Stop buttons
start_clicking_button = tk.Button(new_tab, text="Start Clicking", bg="lightgreen")
start_clicking_button.grid(row=3, column=0, columnspan=2, pady=10)

stop_clicking_button = tk.Button(new_tab, text="Stop Clicking", bg="lightcoral", state=tk.DISABLED)
stop_clicking_button.grid(row=3, column=2, columnspan=2, pady=10)

# Click count display
click_count_var = tk.StringVar(value="Clicks: 0")
click_count_label = tk.Label(new_tab, textvariable=click_count_var)
click_count_label.grid(row=4, column=0, columnspan=4, pady=5)

# Log viewer for mouse clicker
mouse_log_viewer = scrolledtext.ScrolledText(new_tab, width=50, height=10)
mouse_log_viewer.grid(row=5, column=0, columnspan=4, pady=10)

def random_key_press():
    global key_press_count
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    key = random.choice(keys)
    pydirectinput.press(key)
    with lock:
        key_press_count += 1

def run_for_duration(duration):
    global stop_threads
    if duration == 0:
        while not stop_threads:
            random_key_press()
            sleep(random.uniform(0.001, 0.005))
    else:
        end_time = time() + duration
        while time() < end_time and not stop_threads:
            random_key_press()
            sleep(random.uniform(0.001, 0.005))

def start_thread(duration):
    thread = threading.Thread(target=run_for_duration, args=(duration,))
    thread.start()
    return thread

def start_threads(duration, num_threads):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=run_for_duration, args=(duration,))
        thread.start()
        threads.append(thread)
    logging.debug(f"Started {num_threads} threads for random key presses")
    for thread in threads:
        thread.join()
    if duration != 0:
        stop()

def stop_all_threads():
    global stop_threads
    stop_threads = True
    logging.error("\033----- Stop -----\033")
    logging.info(f"Total key presses: {key_press_count}")

def update_run_time(duration):
    if duration == 0:
        count = 0
        def count_up():
            nonlocal count
            if not stop_threads:
                run_time_var.set(str(count))
                count += 1
                root.after(1000, count_up)
        count_up()
    else:
        count = duration
        def count_down():
            nonlocal count
            if count > 0 and not stop_threads:
                run_time_var.set(str(count))
                count -= 1
                root.after(1000, count_down)
        count_down()

def start():
    global stop_threads
    global start_run_time
    stop_threads = False
    num_threads = int(num_threads_entry.get())
    run_time = int(run_time_entry.get())
    start_run_time = run_time
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    num_threads_entry.config(state=tk.DISABLED)
    run_time_entry.config(state=tk.DISABLED)
    threading.Thread(target=start_threads, args=(run_time, num_threads)).start()
    update_run_time(run_time)
    
def stop():
    stop_all_threads()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    num_threads_entry.config(state=tk.NORMAL)
    run_time_entry.config(state=tk.NORMAL)
    run_time_var.set(str(start_run_time))

# --- Mouse Position Clicker Logic ---

clicking_thread = None
stop_clicking_flag = threading.Event()
click_count = 0

def set_mouse_clicker_ui_state(is_clicking):
    state = tk.DISABLED if is_clicking else tk.NORMAL
    start_state = tk.DISABLED if is_clicking else tk.NORMAL
    stop_state = tk.NORMAL if is_clicking else tk.DISABLED

    mouse_x_entry.config(state=state)
    mouse_y_entry.config(state=state)
    get_mouse_pos_button.config(state=state)
    interval_entry.config(state=state)
    start_clicking_button.config(state=start_state)
    stop_clicking_button.config(state=stop_state)

mouse_hook = None

def get_mouse_position_loop():
    while get_mouse_pos_var.get():
        x, y = pydirectinput.position()
        mouse_x_entry.delete(0, tk.END)
        mouse_x_entry.insert(0, str(x))
        mouse_y_entry.delete(0, tk.END)
        mouse_y_entry.insert(0, str(y))
        sleep(0.1)

def stop_getting_pos():
    global mouse_hook
    if get_mouse_pos_var.get():
        get_mouse_pos_var.set(False)
        get_mouse_pos_button.config(text="Get Mouse Position (Ctrl+G or Left Click to Stop)")
        if mouse_hook:
            mouse.unhook(mouse_hook)
            mouse_hook = None

def toggle_get_mouse_position():
    global mouse_hook
    if not get_mouse_pos_var.get():
        get_mouse_pos_var.set(True)
        get_mouse_pos_button.config(text="Stop Getting Mouse Position (Ctrl+G or Left Click)")
        mouse_hook = mouse.on_click(stop_getting_pos)
        threading.Thread(target=get_mouse_position_loop, daemon=True).start()
    else:
        stop_getting_pos()

keyboard.add_hotkey('ctrl+g', toggle_get_mouse_position)

def emergency_stop():
    """Stops all running processes in both tabs. Can be called from a hotkey."""
    global stop_threads
    logging.info("Emergency stop hotkey pressed. Stopping all actions.")
    stop_threads = True # For the first tab
    stop_clicking_flag.set() # For the second tab

keyboard.add_hotkey('F12', emergency_stop)


get_mouse_pos_button.config(command=toggle_get_mouse_position)

def click_loop():
    global click_count
    try:
        interval = float(interval_entry.get())
        x = int(mouse_x_entry.get())
        y = int(mouse_y_entry.get())

        while not stop_clicking_flag.is_set():
            pydirectinput.click(x, y)
            with lock:
                click_count += 1
            
            click_count_var.set(f"Clicks: {click_count}")
            stop_clicking_flag.wait(interval)

    except ValueError:
        logging.error("Invalid input for interval, X or Y coordinate.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        root.after(0, set_mouse_clicker_ui_state, False)

def start_clicking():
    global click_count
    try:
        x = int(mouse_x_entry.get())
        y = int(mouse_y_entry.get())
    except ValueError:
        logging.error("Invalid X or Y coordinate. Please enter a number.")
        return

    logging.info("Starting clicks in 5 seconds. Please focus your target window.")
    root.after(100, lambda: threading.Thread(target=_start_clicking_thread, daemon=True).start())

def _start_clicking_thread():
    sleep(5)
    click_count = 0
    click_count_var.set("Clicks: 0")
    stop_clicking_flag.clear()
    set_mouse_clicker_ui_state(True)
    global clicking_thread
    clicking_thread = threading.Thread(target=click_loop, daemon=True)
    clicking_thread.start()

def stop_clicking():
    stop_clicking_flag.set()
    if clicking_thread:
        clicking_thread.join(timeout=1) # Wait for the thread to finish

start_clicking_button.config(command=start_clicking)
stop_clicking_button.config(command=stop_clicking)

tk.Label(auto_clicker_tab, text="Number of Threads:").grid(row=0, column=0)
num_threads_entry = tk.Entry(auto_clicker_tab)
num_threads_entry.grid(row=0, column=1)
num_threads_entry.insert(0, "1")

tk.Label(auto_clicker_tab, text="Run Time (seconds):").grid(row=1, column=0)
run_time_entry = tk.Entry(auto_clicker_tab, textvariable=run_time_var)
run_time_entry.grid(row=1, column=1)
run_time_var.set("0")

start_button = tk.Button(auto_clicker_tab, text="Start", command=start, width=15, height=2)
start_button.grid(row=2, column=0)

stop_button = tk.Button(auto_clicker_tab, text="Stop", command=stop, state=tk.DISABLED, bg="lightcoral", width=15, height=2)
stop_button.grid(row=2, column=1)

log_viewer = scrolledtext.ScrolledText(auto_clicker_tab, width=50, height=10)
log_viewer.grid(row=3, column=0, columnspan=2)

class TextHandler(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.widget = widget
        self.setFormatter(logging.Formatter('%(asctime)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.widget.configure(state='normal')
            self.widget.insert(tk.END, msg + '\n')
            self.widget.configure(state='disabled')
            self.widget.yview(tk.END)
        self.widget.after(0, append)

text_handler = TextHandler(log_viewer)
logging.getLogger().addHandler(text_handler)

mouse_text_handler = TextHandler(mouse_log_viewer)
logging.getLogger().addHandler(mouse_text_handler)

root.mainloop()
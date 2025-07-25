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
tab_control.add(new_tab, text='Coming Soon')

tab_control.pack(expand=1, fill="both")

run_time_var = StringVar()

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

root.mainloop()
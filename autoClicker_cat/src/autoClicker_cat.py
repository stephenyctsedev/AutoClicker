from time import sleep, time
import random
import logging
import pydirectinput
import threading
import keyboard
import tkinter as tk
from tkinter import scrolledtext

logging.basicConfig(level=logging.DEBUG)

stop_threads = False
key_press_count = 0
lock = threading.Lock()

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
    logging.debug(f"Started {num_threads} threads with run time: {'infinite' if duration == 0 else duration} seconds ...")
    for thread in threads:
        thread.join()
    if duration != 0:
        logging.info(f"Total key presses: {key_press_count}")

def stop_all_threads():
    global stop_threads
    stop_threads = True
    logging.error("\033----- Stop -----\033")
    logging.info(f"Total key presses: {key_press_count}")

def start():
    global stop_threads
    stop_threads = False
    num_threads = int(num_threads_entry.get())
    run_time = int(run_time_entry.get())
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    num_threads_entry.config(state=tk.DISABLED)
    run_time_entry.config(state=tk.DISABLED)
    threading.Thread(target=start_threads, args=(run_time, num_threads)).start()

def stop():
    stop_all_threads()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    num_threads_entry.config(state=tk.NORMAL)
    run_time_entry.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Auto Clicker")

tk.Label(root, text="Number of Threads:").grid(row=0, column=0)
num_threads_entry = tk.Entry(root)
num_threads_entry.grid(row=0, column=1)
num_threads_entry.insert(0, "20")

tk.Label(root, text="Run Time (seconds):").grid(row=1, column=0)
run_time_entry = tk.Entry(root)
run_time_entry.grid(row=1, column=1)
run_time_entry.insert(0, "0")

start_button = tk.Button(root, text="Start", command=start, width=15, height=2)
start_button.grid(row=2, column=0)

stop_button = tk.Button(root, text="Stop", command=stop, state=tk.DISABLED, bg="lightcoral", width=15, height=2)
stop_button.grid(row=2, column=1)

log_viewer = scrolledtext.ScrolledText(root, width=50, height=10)
log_viewer.grid(row=3, column=0, columnspan=2)

class TextHandler(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.widget = widget

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
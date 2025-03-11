from time import sleep, time
import random
import logging
import pydirectinput
import threading
import keyboard

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
    # logging.debug(f"Thread ID: {threading.get_ident()} - Key: {key}")

def run_for_duration(duration):
    global stop_threads
    if duration == 0:
        while not stop_threads:
            random_key_press()
            sleep(random.uniform(0.001, 0.005))  # Adjust sleep duration to a range of 0.001 to 0.005 seconds
    else:
        end_time = time() + duration
        while time() < end_time and not stop_threads:
            random_key_press()
            sleep(random.uniform(0.001, 0.005))  # Adjust sleep duration to a range of 0.001 to 0.005 seconds

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
    return threads

def stop_all_threads():
    global stop_threads
    stop_threads = True
    logging.error("\033[91mStop Hot Key Detected\033[0m")  # Log in red color
    logging.info(f"Total key presses: {key_press_count}")

# Example usage
if __name__ == "__main__":
    max_threads = 100  # Set a reasonable maximum number of threads
    print(f"Maximum number of threads you can set: {max_threads}")

    num_threads = input("Enter the number of threads (default 20): ")
    num_threads = int(num_threads) if num_threads else 20
    if num_threads > max_threads:
        print(f"Number of threads exceeds the maximum limit of {max_threads}. Setting to {max_threads}.")
        num_threads = max_threads

    run_time = input("Enter the duration of the script in seconds (0 for infinite, default 0): ")
    run_time = int(run_time) if run_time else 0

    threads = start_threads(run_time, num_threads)  # Run for seconds in multiple threads

    # Set up a keyboard shortcut to stop all threads
    keyboard.add_hotkey('esc', stop_all_threads)

    for thread in threads:
        thread.join()  # Wait for all threads to complete

    # Show key press count when the run time finishes
    if run_time != 0:
        logging.info(f"Total key presses: {key_press_count}")
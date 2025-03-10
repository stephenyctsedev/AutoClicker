from time import sleep, time
import random
import logging
import pydirectinput

logging.basicConfig(level=logging.DEBUG)

def random_key_press():
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    key = random.choice(keys)
    pydirectinput.press(key)
    logging.debug("Key: " + key)

def run_for_duration(duration):
    if duration == 0:
        while True:
            random_key_press()
            sleep(0.001)  # Further reduce sleep duration to make the loop faster
    else:
        end_time = time() + duration
        while time() < end_time:
            random_key_press()
            sleep(0.001)  # Further reduce sleep duration to make the loop faster

# Example usage
if __name__ == "__main__":
    run_for_duration(0)  # Run indefinitely
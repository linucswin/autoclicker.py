import time
import threading
import pydirectinput
import tkinter as tk

keys_sequence = ['w', 'a', 's', 'd']  # Define the keys sequence
sequence_index = 0

def press_key(key):
    pydirectinput.keyDown(key)
    time.sleep(0.2)  # Simulate holding the key for 0.2 second
    pydirectinput.keyUp(key)
    log_text.insert(tk.END, "{} key pressed at: {}\n".format(key.upper(), time.strftime("%H:%M:%S")))

def press_keys_periodically(interval, stop_event):
    global sequence_index
    while not stop_event.is_set():
        key = keys_sequence[sequence_index]
        press_key(key)

        sequence_index = (sequence_index + 1) % len(keys_sequence)  # Move to the next key
        log_text.insert(tk.END, "Next move in {} seconds...\n".format(interval))
        time.sleep(interval)

def start_script():
    global stop_script_event, sequence_index
    stop_script_event.clear()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    log_text.insert(tk.END, "The script was started.\n")

    # Start with the first key in the sequence
    sequence_index = 0

    t = threading.Thread(target=press_keys_periodically, args=(interval, stop_script_event))
    t.daemon = True
    t.start()

def stop_script():
    global stop_script_event
    stop_script_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    log_text.insert(tk.END, "The script was stopped.\n")

if __name__ == "__main__":
    # Set the interval in seconds (1 minute and 25 seconds)
    interval = 1 * 60 + 25
    stop_script_event = threading.Event()

    # Create GUI
    app = tk.Tk()
    app.title("Autoclicker for Liberty.MP made by 01001100 01001001 01001110 01010101 01011000")

    log_text = tk.Text(app, wrap=tk.WORD, width=40, height=10)
    log_text.pack(padx=10, pady=10)

    start_button = tk.Button(app, text="Start", command=start_script)
    start_button.pack(side=tk.LEFT, padx=10, pady=5)

    stop_button = tk.Button(app, text="Stop", command=stop_script, state=tk.DISABLED)
    stop_button.pack(side=tk.RIGHT, padx=10, pady=5)

    try:
        app.mainloop()
    except KeyboardInterrupt:
        stop_script()

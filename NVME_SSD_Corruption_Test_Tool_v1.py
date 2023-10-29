import os
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from threading import Thread, Event
import time

# Constants
CHUNK_SIZE = 1024 * 1024  # 1 MB
FILE_NAME = "large_file.bin"

def generate_random_bytes(size):
    return os.urandom(size)

def md5_checksum(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    return md5_hash.digest()

def write_chunk_with_checksum(file, data, checksum):
    file.write(data)
    file.write(checksum)

def verify_chunk(data, checksum):
    return md5_checksum(data) == checksum

def run_test(gbytes, test_ram_only, progress_var, status_var, time_var, stop_event, start_button, details_frame, root):
    total_chunks = gbytes * 1024  # Convert GB to number of 1 MB chunks
    progress_var.set(0)
    status_var.set("Running...")
    details_frame.pack(pady=5)  # Show details when test starts
    start_time = time.time()
    written_gb = 0
    read_gb = 0

    try:
        if test_ram_only:
            ok_count = 0
            for i in range(total_chunks):
                if stop_event.is_set():
                    break
                chunk = generate_random_bytes(CHUNK_SIZE)
                checksum = md5_checksum(chunk)
                if verify_chunk(chunk, checksum):
                    ok_count += 1
                progress_var.set((i + 1) / total_chunks * 100)
                update_time_status(i + 1, total_chunks, start_time, time_var, written_gb, read_gb)
            if not stop_event.is_set():
                not_ok_count = total_chunks - ok_count
                status_var.set(f"RAM test completed. {ok_count} chunks OK, {not_ok_count} chunks not OK. ({ok_count/total_chunks*100:.2f}% OK)")
        else:
            with open(FILE_NAME, "wb") as file:
                for i in range(total_chunks):
                    if stop_event.is_set():
                        break
                    chunk = generate_random_bytes(CHUNK_SIZE)
                    checksum = md5_checksum(chunk)
                    write_chunk_with_checksum(file, chunk, checksum)
                    written_gb = (i + 1) * CHUNK_SIZE / (1024 ** 3)
                    progress_var.set((i + 1) / total_chunks * 50)
                    update_time_status(i + 1, total_chunks * 2, start_time, time_var, written_gb, read_gb)

            if not stop_event.is_set():
                ok_count = 0
                with open(FILE_NAME, "rb") as file:
                    for i in range(total_chunks):
                        if stop_event.is_set():
                            break
                        chunk = file.read(CHUNK_SIZE)
                        stored_checksum = file.read(16)  # MD5 checksum size is 16 bytes
                        if verify_chunk(chunk, stored_checksum):
                            ok_count += 1
                        read_gb = (i + 1) * CHUNK_SIZE / (1024 ** 3)
                        progress_var.set(50 + (i + 1) / total_chunks * 50)
                        update_time_status(total_chunks + i + 1, total_chunks * 2, start_time, time_var, written_gb, read_gb)

                if not stop_event.is_set():
                    not_ok_count = total_chunks - ok_count
                    status_var.set(f"File test completed. {ok_count} chunks OK, {not_ok_count} chunks not OK. ({ok_count/total_chunks*100:.2f}% OK)")
    finally:
        start_button.config(text="Start Test")
        details_frame.pack_forget()  # Hide details when test ends
        if not test_ram_only:
            delete_file(root)

def update_time_status(current_chunk, total_chunks, start_time, time_var, written_gb, read_gb):
    elapsed_time = time.time() - start_time
    remaining_time = (elapsed_time / current_chunk) * (total_chunks - current_chunk) if current_chunk > 0 else 0
    time_var.set(f"Time elapsed: {int(elapsed_time)}s\nRemaining: {int(remaining_time)}s\nWritten: {written_gb:.2f} GB\nRead: {read_gb:.2f} GB")

def delete_file(root):
    if os.path.exists(FILE_NAME):
        try:
            os.remove(FILE_NAME)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to delete file: {e}", parent=root)


def start_or_abort_test(progress_var, status_var, time_var, start_button, stop_event, details_frame, root):
    if start_button["text"] == "Start Test":
        gbytes = simpledialog.askinteger("Input", "How many GBs do you want to test?", minvalue=1, maxvalue=1024, parent=root)
        if gbytes is None:
            return

        test_ram_only = messagebox.askyesno("Choose Test Mode", "Do you want to test only RAM?", parent=root)
        stop_event.clear()
        Thread(target=run_test, args=(gbytes, test_ram_only, progress_var, status_var, time_var, stop_event, start_button, details_frame, root)).start()
        start_button["text"] = "Abort Test"
    else:
        stop_event.set()
        status_var.set("Test aborted.")
        start_button["text"] = "Start Test"

def on_closing(root, stop_event):
    if messagebox.askokcancel("Quit", "Are you sure you want to quit? This will stop any ongoing tests.", parent=root):
        stop_event.set()
        root.after(500, check_and_close, root, stop_event)

def check_and_close(root, stop_event):
    if not stop_event.is_set():
        root.after(500, check_and_close, root, stop_event)
    else:
        delete_file(root)
        root.destroy()

def main():
    root = tk.Tk()
    root.title("NVME SSD Corruption Test Tool")

    progress_var = tk.DoubleVar()
    status_var = tk.StringVar(value="Ready")
    time_var = tk.StringVar()
    stop_event = Event()

    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', variable=progress_var)
    progress_bar.pack(fill=tk.X, expand=True, padx=20, pady=10)

    status_label = tk.Label(root, textvariable=status_var)
    status_label.pack(pady=5)

    details_frame = tk.Frame(root)
    time_label = tk.Label(details_frame, textvariable=time_var, justify='left')
    time_label.pack()

    creator_label = tk.Label(root, text="Created by Thomas Budicin\n2023")
    creator_label.pack(pady=5)

    start_button = tk.Button(root, text="Start Test", command=lambda: start_or_abort_test(progress_var, status_var, time_var, start_button, stop_event, details_frame, root))
    start_button.pack(pady=20)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, stop_event))

    root.mainloop()

if __name__ == "__main__":
    main()

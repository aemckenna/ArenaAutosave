import tkinter as tk
import time
import logging
import os
from shutil import copyfile

class AutoSaveApp:
    LOG_PATH = "/Users/ashermckenna/Desktop/autosave_log.txt"
    AUTOSAVE_INTERVAL = 15 * 60  # 15 minutes
    ARENA_FILE_PATH = '/Users/ashermckenna/Documents/Resolume Arena/Compositions/Example.avc'

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoSave App")

        # Set the window attributes to stay on top
        self.root.attributes("-topmost", True)

        # Set the initial size of the window
        self.root.geometry("180x80")

        # Set a fixed width for the background label
        fixed_width = -10
        self.background_label = tk.Label(self.root, text="", bg="white", width=fixed_width, height=self.root.winfo_screenheight())
        self.background_label.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        self.label_frame = tk.Frame(self.root, bg="white", width=self.root.winfo_screenwidth() - fixed_width, height=self.root.winfo_screenheight())
        self.label_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.label_frame, text="AutoSave is inactive", bg="white")
        self.label.pack(pady=1)

        self.start_button = tk.Button(self.label_frame, text="Start AutoSave", command=self.start_autosave, bg="grey")
        self.start_button.pack(pady=1)

        self.stop_button = tk.Button(self.label_frame, text="Stop AutoSave", command=self.stop_autosave, bg="grey")
        self.stop_button.pack(pady=1)


        self.is_autosaving = False
        self.autosave_interval = 15 * 60  # 15 minutes
        self.arena_file_path = '/Users/ashermckenna/Documents/Resolume Arena/Compositions/Example.avc'
        log_path  = "/Users/ashermckenna/Desktop/autosave_log.txt"
        logging.basicConfig(filename=self.LOG_PATH, level=logging.INFO, format='%(asctime)s - %(message)s')

        # Add console logging for debugging during development
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(console_handler)

    def start_autosave(self):
        if not self.is_autosaving:
            self.is_autosaving = True
            self.label.config(text="AutoSave is active")
            self.background_label.config(bg="red")  # Set background color to red
            self.autosave_loop()

            self.start_button.config(bg="green")
            self.stop_button.config(bg="green")

    def stop_autosave(self):
        if self.is_autosaving:
            self.is_autosaving = False
            self.label.config(text="AutoSave is stopped")
            self.background_label.config(bg="white")  # Reset to default background color
            self.start_button.config(bg="grey")
            self.stop_button.config(bg="grey")

    def autosave_loop(self):
        if self.is_autosaving:
            try:
                # Duplicate the file before saving
                self.duplicate_file()

                self.label.config(text="AutoSave triggered for Arena")
                logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - AutoSave triggered for Arena")

            except Exception as e:
                self.label.config(text=f"Error: {str(e)}")

            # Schedule the next autosave action after the specified interval
            self.root.after(int(self.autosave_interval * 1000), self.autosave_loop)

    def duplicate_file(self):
        try:
            # Get the directory and filename from the provided path
            directory, filename = os.path.split(self.arena_file_path)
            # Extract the file extension
            base, ext = os.path.splitext(filename)

            # Find the latest numbered file in the directory
            existing_files = [f for f in os.listdir(directory) if f.startswith(f"{base}_autosave_") and f.endswith(ext)]
            existing_numbers = [int(f.split('_')[-1].split('.')[0]) for f in existing_files]

            if existing_numbers:
                # Use the maximum existing number and increment it
                next_number = max(existing_numbers) + 1
            else:
                # If no existing numbers, start from 1
                next_number = 1

            # Create a new filename with the incremented number
            new_filename = f"{base}_autosave_{next_number}{ext}"

            # Build the full path for the new file
            new_filepath = os.path.join(directory, new_filename)

            # Copy the file to the new location
            copyfile(self.arena_file_path, new_filepath)

            logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - File duplicated: {new_filepath}")

        except Exception as e:
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error duplicating file: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoSaveApp()
    app.run()
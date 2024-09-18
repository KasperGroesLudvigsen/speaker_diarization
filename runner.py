import os
import time
import threading

class FileProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_list = []
        self.update_interval = 300  # 5 minutes (300 seconds)
        self.lock = threading.Lock()

        # Start a background thread to update the file list every 5 minutes
        self.update_thread = threading.Thread(target=self._update_file_list_periodically)
        self.update_thread.daemon = True
        self.update_thread.start()

    def _update_file_list_periodically(self):
        """Update the file list every `update_interval` seconds."""
        while True:
            self.update_file_list()
            time.sleep(self.update_interval)

    def update_file_list(self):
        """Update the file list with the current files in the folder, sorted by creation time (oldest first)."""
        with self.lock:
            # Get list of files in the folder
            current_files = [
                f for f in os.listdir(self.folder_path)
                if os.path.isfile(os.path.join(self.folder_path, f))
            ]
            # Sort files by creation time (oldest first)
            current_files.sort(key=lambda f: os.path.getctime(os.path.join(self.folder_path, f)))
            self.file_list = current_files
            print(f"Updated file list (oldest first): {self.file_list}")

    def process_files(self):
        """Process files in a FIFO (oldest first) order."""
        while True:
            with self.lock:
                if not self.file_list:
                    print("No files to process.")
                    break

                # Pop the first file (oldest) from the list
                file_to_process = self.file_list.pop(0)
            
            # Simulate file processing
            self._process_file(file_to_process)

    def _process_file(self, file_name):
        """Simulate processing of a single file."""
        print(f"Processing file: {file_name}")
        # Simulate file processing (you can replace this with actual processing logic)
        time.sleep(1)
        print(f"Finished processing file: {file_name}")

# Example usage:
# folder_path = "/path/to/your/folder"
# processor = FileProcessor(folder_path)
# processor.process_files()

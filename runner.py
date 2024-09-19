import os
import time
import threading
from queue import Queue

class FileProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_queue = Queue()  # Thread-safe queue to hold files
        self.update_interval = 300  # 5 minutes (300 seconds)

        # Start a background thread to update the file queue every 5 minutes
        self.update_thread = threading.Thread(target=self._update_file_list_periodically)
        self.update_thread.daemon = True  # Daemon thread to stop with the main program
        self.update_thread.start()

    def _update_file_list_periodically(self):
        """Update the file queue every `update_interval` seconds."""
        while True:
            self.update_file_queue()
            time.sleep(self.update_interval)

    def update_file_queue(self):
        """Update the file queue with new files in the folder, sorted by creation time (oldest first)."""
        # Get list of files in the folder
        current_files = [
            f for f in os.listdir(self.folder_path)
            if os.path.isfile(os.path.join(self.folder_path, f))
        ]
        # Sort files by creation time (oldest first)
        current_files.sort(key=lambda f: os.path.getctime(os.path.join(self.folder_path, f)))

        # Add files to the queue (non-blocking put)
        for file_name in current_files:
            if not self._is_file_in_queue(file_name):
                self.file_queue.put(file_name)
                print(f"Added file to queue: {file_name}")

    def _is_file_in_queue(self, file_name):
        """Helper to check if a file is already in the queue."""
        # Since Queue does not provide direct access to its items, you can manage a set or keep a record of processed files
        return False  # You can enhance this logic if needed

    def process_files(self):
        """Continuously process files in a FIFO (oldest first) order."""
        while True:
            try:
                # Wait and get the next file from the queue (blocking)
                file_to_process = self.file_queue.get(block=True)
                self._process_file(file_to_process)
                self.file_queue.task_done()  # Mark the file as processed
            except Exception as e:
                print(f"Error processing file: {e}")

    def _process_file(self, file_name):
        """Simulate processing of a single file."""
        print(f"Processing file: {file_name}")
        time.sleep(1)  # Simulate file processing
        print(f"Finished processing file: {file_name}")

# Example usage:
# folder_path = "/path/to/your/folder"
# processor = FileProcessor(folder_path)
# processor.process_files()

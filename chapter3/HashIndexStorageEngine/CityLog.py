import threading
import queue
import log_pb2
import struct
import time


class CityLog:
    def __init__(self, filename):
        self.filename = filename
        # if filename doesn't exist, create it
        open(filename, "a").close()
        self.log_queue = queue.Queue()
        self.write_queue = queue.Queue()
        self.index = {}
        self.last_offset = 0
        self.reader_thread = threading.Thread(target=self._reader_thread, daemon=True)
        self.writer_thread = threading.Thread(target=self._writer_thread, daemon=True)

    def start(self):
        self.reader_thread.start()
        self.writer_thread.start()

    def stop(self):
        # Signal the threads to stop gracefully
        self.write_queue.put(None)
        self.reader_thread.join()
        self.writer_thread.join()

    def add_entry(self, city_name, population, land_area):
        log_entry = log_pb2.CityLogEntry()
        log_entry.city_name = city_name
        log_entry.city_info.population = population
        log_entry.city_info.land_area = land_area
        self.write_queue.put(log_entry)

    def get_entry(self, city_name):
        offset = self.index.get(city_name)
        if offset is None:
            return None
        with open(self.filename, "rb") as f:
            f.seek(offset)
            length_prefix = f.read(8)
            message_length = struct.unpack("<Q", length_prefix)[0]
            log_entry = log_pb2.CityLogEntry.FromString(f.read(message_length))
            return log_entry

    def _reader_thread(self):
        with open(self.filename, "rb") as f:
            while True:
                length_prefix = f.read(8)
                if not length_prefix:
                    # End of file, wait for more data to be written
                    time.sleep(0.1)
                    continue
                message_length = struct.unpack("<Q", length_prefix)[0]
                log_entry = log_pb2.CityLogEntry.FromString(f.read(message_length))
                self.index[log_entry.city_name] = self.last_offset
                self.last_offset = f.seek(self.last_offset + 8 + message_length)
                self.log_queue.put(log_entry)

    def _writer_thread(self):
        with open(self.filename, "ab") as f:
            while True:
                log_entry = self.write_queue.get()
                if log_entry is None:
                    # None sentinel means to stop the thread
                    break
                log_entry_data = log_entry.SerializeToString()
                f.write(struct.pack("<Q", len(log_entry_data)))
                f.write(log_entry_data)
                f.flush()
                self.write_queue.task_done()

    def start_repl(self):
        while True:
            command = input("Enter command (add/get/exit): ")
            if command == "add":
                city_name = input("Enter city name: ")
                population = int(input("Enter population: "))
                land_area = float(input("Enter land area: "))
                self.add_entry(city_name, population, land_area)
                print(f"Added entry for {city_name}")
            elif command == "get":
                city_name = input("Enter city name: ")
                log_entry = self.get_entry(city_name)
                if log_entry:
                    print(f"Population of {log_entry.city_name}: {log_entry.city_info.population}")
                else:
                    print(f"No entry found for {city_name}")
            elif command == "exit":
                break
            else:
                print("Invalid command")
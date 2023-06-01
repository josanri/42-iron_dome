import os
import threading
import sys
import logging
import argparse
import daemon
import datetime
import psutil
import time
import pathlib
import math

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logfile = '/var/log/irondome/irondome.log'

class IronDome:
    class IronDomeMemoryUsage(threading.Thread):
        def __init__(self) -> None:
            super(IronDome.IronDomeMemoryUsage, self).__init__(daemon=True)
        def run(self):
            process = psutil.Process()
            while True:
                mib_usage = process.memory_info().rss / 1024 ** 2
                if mib_usage < 100:
                    logging.info(f"Memory usage of: {mib_usage} MiB")
                else:
                    os.exit(1)
                time.sleep(1.23)
    class IronDomeEventHandler(FileSystemEventHandler):
        def __init__(self, path):
            path_obj = pathlib.Path(path)
            path_obj.rglob("*")
        def calculate_entropy_of_a_file(filename:str):
            entropy = 0
            filesize = os.stat(filename).st_size
            with open(filename, 'rb') as file:
                byte_counts = file.read(256)
                for count in byte_counts:
                    # If no bytes of this value were seen in the value, it doesn't affect
                    # the entropy of the file.
                    if count == 0:
                        continue
                    # p is the probability of seeing this byte in the file, as a floating-
                    # point number
                    p = 1.0 * count / total
                    entropy -= p * math.log(p, 256)
        def on_created(self, event):
            logging.info(f"{event} {event.src_path} creado")
        def on_modified(self, event):
            logging.info(f"{event} {event.src_path} modificado")

def main_program(path):
    logging.basicConfig(level=logging.INFO, filename=logfile)
    logging.info(f"Starting to log at {datetime.datetime.now()}")

    observer = Observer()
    observer.schedule(IronDome.IronDomeEventHandler(), path, recursive=False)
    observer.start()
    memory_usage_thread = IronDome.IronDomeMemoryUsage(path)
    memory_usage_thread.start()

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    memory_usage_thread.stop()
    memory_usage_thread.join()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Tried to execute the program without being root")
        exit(1)
    if not os.path.exists("/var/log/irondome"):
        os.makedirs("/var/log/irondome")
    parser = argparse.ArgumentParser(description='Iron Dome, ./iron_dome --path directory')
    parser.add_argument('--path', type=str, help="Directory where iron_dome will check the activity")
    args = parser.parse_args()
    if not os.path.exists(args.path):
        logging.error(f"Tried to execute on a path that does not exist {args.path}")
        exit(1)
    with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
        main_program(args.path)
import os
import threading
import sys
import logging
import argparse
import daemon

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logfile = '/var/log/irondome/irondome.log'

class IronDome(threading.Thread):
    class IronDomeEventHandler(FileSystemEventHandler):
        def on_modified(self, event):
            print(event.src_path, "modificado.")
    def __init__(self, event) -> None:
        super(IronDome, self).__init__(daemon=True)
        self.event = event  
        logging.info("Starting to log")
    def run(self):
        while not self.event.is_set():
            self.event.wait(1)


def main_program():
    print("HEY")
    if not os.path.exists("/var/log/irondome"):
        os.makedirs("/var/log/irondome")
    logging.basicConfig(level=logging.INFO, filename=logfile)
    parser = argparse.ArgumentParser(description='Iron Dome, ./iron_dome --path directory')
    parser.add_argument('--path', type=str, help="Directory where iron_dome will check the activity")
    args = parser.parse_args()
    if not os.path.exists(args.path):
        logging.error(f"Tried to execute on a path that does not exist {args.path}")
        exit(1)
    else:
        print("Daemon")
        try:
            event = threading.Event()
            iron_dome = IronDome(event)
            iron_dome.start()
            iron_dome.join()
        except KeyboardInterrupt:
            event.set()
            iron_dome.join()
        print("EXITING the program")

def daemonize_program():
    with daemon.DaemonContext():
        print("HEY")
        main_program()

if __name__ == "__main__":
    # if os.geteuid() != 0:
    #     logging.error("Tried to execute the program without being root")
    #     exit(1)
    daemonize_program()
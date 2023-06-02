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
import mimetypes
import collections

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ransom_ext = (".micro", ".zepto", ".cerber", ".locky", ".cerber3", ".cryp1", ".mole", ".onion", ".axx", ".osiris", ".crypz", ".crypt", ".locked", ".odin", ".ccc", ".cerber2", ".sage", ".globe", ".exx", ".good", ".wallet", ".1txt", ".decrypt2017", ".encrypt", ".ezz", ".zzzzz", ".MERRY", ".enciphered", ".r5a", ".aesir", ".ecc", ".enigma", ".cryptowall", ".encrypted", ".loli", ".breaking_bad", ".coded", ".ha3", ".damage", ".wcry", ".lol!", ".cryptolocker", ".dharma", ".MRCR1", ".sexy", ".crjoker", ".fantom", ".keybtc@inbox_com", ".rrk", ".legion", ".kratos", ".LeChiffre", ".kraken", ".zcrypt", ".maya", ".enc", ".file0locked", ".crinf", ".serp", ".potato", ".ytbl", ".surprise", ".angelamerkel", ".windows10", ".lesli", ".serpent", ".PEGS1", ".dale", ".pdcr", ".zzz", ".xyz", ".1cbu1", ".venusf", ".coverton", ".thor", ".rnsmwr", ".evillock", ".R16m01d05", ".wflx", ".nuclear55", ".darkness", ".encr", ".rekt", ".kernel_time", ".zyklon", ".Dexter", ".locklock", ".cry", ".VforVendetta", ".btc", ".raid10", ".dCrypt", ".zorro", ".AngleWare", ".EnCiPhErEd", ".purge", ".realfs0ciety@sigaint.org.fs0ciety", ".shit", ".atlas", ".exotic", ".crypted", ".padcrypt", ".xxx", ".hush", ".bin", ".vbransom", ".RMCM1", ".cryeye", ".unavailable", ".braincrypt", ".fucked", ".crypte", "._AiraCropEncrypted", ".stn", ".paym", ".spora", ".dll", ".RARE1", ".alcatraz", ".pzdc", ".aaa", ".encrypted", ".ttt", ".odcodc", ".vvv", ".ruby", ".pays", ".comrade", ".enc", ".abc", ".xxx", ".antihacker2017", ".herbst", ".szf", ".rekt", ".bript", ".crptrgr", ".kkk", ".rdm", ".BarRax", ".vindows", ".helpmeencedfiles", ".hnumkhotep", ".CCCRRRPPP", ".kyra", ".fun", ".rip", ".73i87A", ".bitstak", ".kernel_complete", ".payrms", ".a5zfn", ".perl", ".noproblemwedecfiles", ".lcked", ".p5tkjw", ".paymst", ".magic", ".payms", ".d4nk", ".SecureCrypted", ".paymts", ".kostya", ".lovewindows", ".madebyadam", ".powerfulldecrypt", ".gefickt", ".kernel_pid", ".ifuckedyou", ".grt", ".conficker", ".edgel", ".PoAr2w", ".oops", ".adk", ".encrypted", ".Whereisyourfiles", ".czvxce", ".theworldisyours", ".info", ".razy", ".rmd", ".fun", ".kimcilware", ".paymrss", ".dxxd", ".pec", ".rokku", ".lock93", ".vxlock", ".pubg", ".crab")
logfile = '/var/log/irondome/irondome.log'

def read_procfs():
        with open("/proc/diskstats") as f:
            lines = f.readlines()
        result = 0
        for line in lines:
            fields = line.split()
            result += int(fields[9])
        return result

class IronDome:
    class IronDomeMemoryAndDiskUsage(threading.Thread):
        def __init__(self) -> None:
            super(IronDome.IronDomeMemoryAndDiskUsage, self).__init__(daemon=True)

        def run(self):
            process = psutil.Process()
            while True:
                mib_usage = process.memory_info().rss / 1024 ** 2
                if mib_usage < 100:
                    logging.info(f"Memory usage of this process: {mib_usage} MiB")
                else:
                    logging.error(f"Memory usage of this process: {mib_usage} MiB")
                    os.exit(1)
                cpu_usage = psutil.cpu_percent(1)
                if cpu_usage > 90.0:
                    logging.warning(f"High CPU usage - {cpu_usage}%")
                else:
                    logging.info(f"CPU usage - {cpu_usage}%")
                time.sleep(1.23)
    class IronDomeDiskAbuse(threading.Thread):
        def __init__(self) -> None:
            super(IronDome.IronDomeDiskAbuse, self).__init__(daemon=True)
        def run(self):
            previous_read_time = read_procfs()
            while True:
                new_read_time = read_procfs()
                if previous_read_time - new_read_time > 800:
                    logging.warning(f"High level of read")
                logging.info(f"Disk read percentage {(new_read_time - new_read_time) / 1000} %")
                previous_read_time = new_read_time
                time.sleep(1)
    class IronDomeEventHandler(FileSystemEventHandler):
        entropy_change_limit = 0.25

        def __init__(self, path, extensions):
            self.extensions = extensions
            self.file_dict = dict()
            for file in pathlib.Path(path).rglob("*"):
                if self.extensions != None and pathlib.Path(file).suffix not in self.extensions:
                    break
                try:
                    logging.info(f"{file}")
                    self.file_dict[file] = IronDome.IronDomeEventHandler.calculate_entropy_of_a_file(file)
                except Exception as err:
                    logging.error(f"Could not calculate the entropy of {file} - {err}")

        def calculate_entropy_of_a_file(filename:str):
            entropy = 0
            filesize = os.stat(filename).st_size
            with open(filename, 'rb') as file:
                byte_read  = True
                cnt = collections.Counter()
                while byte_read:
                    byte_read = file.read(4096)
                    cnt.update(byte_read)
                for count in cnt.values():
                    if count == 0:
                        continue
                    p = 1.0 * count / filesize
                    entropy -= p * math.log(p, 256)
            return entropy
        
        def warn_extension_mismatch(filename):
            file_extension = pathlib.Path(filename).suffix
            if (file_extension in ransom_ext):
                logging.warning(f"{filename} is a suspicious extension for a file")
            # mime_extension = mimetypes.guess_type(filename)[0]
            # if (mime_extension != None and file_extension not in mimetypes.guess_all_extensions(mime_extension)):
            #     logging.warning(f"{filename} has not the format for the {mime_extension} extension")

        def on_created(self, event):
            if self.extensions != None and pathlib.Path(event.src_path).suffix not in self.extensions:
                return
            if event.is_directory:
                return
            self.file_dict[event.src_path] = IronDome.IronDomeEventHandler.calculate_entropy_of_a_file(event.src_path)
            logging.info(f"{event} {event.src_path} creado")
        def on_moved(self, event):
            if (self.extensions != None 
                and (pathlib.Path(event.src_path).suffix not in self.extensions
                     or pathlib.Path(event.dest_path).suffix not in self.extensions)):
                return
            new_entropy = IronDome.IronDomeEventHandler.calculate_entropy_of_a_file(event.dest_path)
            if self.file_dict.get(event.src_path) != None:
                if abs(new_entropy - self.file_dict[event.src_path]) > IronDome.IronDomeEventHandler.entropy_change_limit:
                    logging.warning(f"{event.dest_path} is a suspicious extension for a file")
                if (self.extensions != None 
                    and pathlib.Path(event.event.src_path).suffix in self.extensions):
                    self.file_dict.pop(event.src_path)
                if (self.extensions != None
                    and pathlib.Path(event.dest_path).suffix in self.extensions):
                    self.file_dict[event.dest_path] = IronDome.IronDomeEventHandler.calculate_entropy_of_a_file(event.dest_path)
            elif (self.extensions != None and pathlib.Path(event.dest_path).suffix in self.extensions):
                    self.file_dict[event.dest_path] = IronDome.IronDomeEventHandler.calculate_entropy_of_a_file(event.dest_path)

            logging.info(f"{event.src_path} -> {event.dest_path} renombrado")
            IronDome.IronDomeEventHandler.warn_extension_mismatch(event.src_path)

        def on_modified(self, event):
            if self.extensions != None and pathlib.Path(event.src_path).suffix not in self.extensions:
                return
            if event.is_directory:
                return
            logging.info(f"{event} {event.src_path} modificado")
            IronDome.IronDomeEventHandler.warn_extension_mismatch(event.src_path)


def main_program(path, extensions):
    logging.basicConfig(level=logging.INFO, filename=logfile)
    logging.info(f"Starting to log at {datetime.datetime.now()}")

    observer = Observer()
    observer.schedule(IronDome.IronDomeEventHandler(path, extensions), path, recursive=True)
    memory_usage_thread = IronDome.IronDomeMemoryAndDiskUsage()
    disk_abuse_thread = IronDome.IronDomeDiskAbuse()
    observer.start()
    memory_usage_thread.start()
    disk_abuse_thread.start()
    observer.join()
    disk_abuse_thread.join()
    memory_usage_thread.join()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Tried to execute the program without being root")
        exit(1)
    if not os.path.exists("/var/log/irondome"):
        os.makedirs("/var/log/irondome")
    parser = argparse.ArgumentParser(description='Iron Dome, ./iron_dome --path directory')
    parser.add_argument('-p', '--path', type=str, help="Directory where iron_dome will check the activity")
    parser.add_argument('-e', '--extensions', nargs='*', help="Extensions to monitor")
    args = parser.parse_args()
    if not os.path.exists(args.path):
        print(f"Tried to execute on a path that does not exist {args.path}")
        exit(1)
    if not os.path.isdir(args.path):
        print(f"Tried to execute on a path that does not correspond to a directory {args.path}")
        exit(1)
    with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
        main_program(args.path, args.extensions)
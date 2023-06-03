import threading


class CPU_Usage(threading.Thread):
        def __init__(self) -> None:
            super(CPU_Usage, self).__init__(daemon=True)

        def run(self):
            x = 0
            while True:
                x += 5
        
thread1 = CPU_Usage()
thread2 = CPU_Usage()
thread3 = CPU_Usage()
thread4 = CPU_Usage()
thread5 = CPU_Usage()
thread6 = CPU_Usage()

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()


thread1.join()
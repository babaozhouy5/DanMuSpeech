# -*- coding: utf-8

import sys
import time
import threading
import subprocess
from utils import which

lock = threading.Lock()

class Player(threading.Thread):

    def __init__(self, queue):
        super(Player, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            lock.acquire()
            if not self.queue.empty():
                voiceStream = self.queue.get()
                playStream(voiceStream)
                lock.release()
            else:
                lock.release()
            time.sleep(1)

def playStream(stream):
    with open("output.mp3", "wb") as fw:
        fw.write(stream)

    fname = "output.mp3" # temp.name
    exe = "ffplay" if sys.platform.find('darwin')>=0 else "ffplay.exe"
    if not which(exe):
        print("ffplay: Executable not found on machine.")
        raise Exception("Dependency not found: %s" % exe)

    command = [which(exe), "-vn", "-nodisp", "-autoexit", "-loglevel", "error", "-i", fname, "-af", "volume=0.5"]
    subprocess.check_output(command)

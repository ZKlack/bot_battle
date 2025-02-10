import os
import subprocess
import shutil
import atexit
import builtins
import threading
import time
import queue

# globals
FILE = None #see "def open(name:str)->None:" and "def print(txt:str, end:str="\n")->int:" for context

SUPPORTED: dict[str,bool] = {
    "python": shutil.which("python") is not None
}

EXTENSIONS: dict[str, any] = {}
if SUPPORTED["python"]:
    EXTENSIONS["py"] = lambda name: ["python", name]

# Functions
def check(name:str)->bool:
    if "." not in name:
        return False
    if name.rsplit(".", 1)[-1] not in EXTENSIONS:
        return False
    return os.path.exists(name)

def gethandle(name:str)->list[str]|None:
    ext = name.rsplit(".",1)[-1]
    if ext not in EXTENSIONS:
        return None
    return EXTENSIONS[ext](name)

def start(name:str|list[str])->subprocess.Popen|None|list[subprocess.Popen|None]:
    if not isinstance(name,str):
        return [start(i) for i in name]
    if not check(name):
        return None
    handle = gethandle(name)

    result = subprocess.Popen(
        handle,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8"
    )
    atexit.register(lambda p=result: close(p))
    return result

def write(prcc:subprocess.Popen|list[subprocess.Popen], msg:str)->None:
    if not isinstance(prcc,subprocess.Popen):
        for i in prcc:
            write(i,msg)
        return None
    msg=str(msg)
    if not msg.endswith("\n"):
        msg=msg+"\n"
    prcc.stdin.write(msg)
    prcc.stdin.flush()

def enqueue_output(pipe, output_queue):
    try:
        for line in iter(pipe.readline, ''):
            output_queue.put(line.strip())
    except Exception:
        pass
    finally:
        pipe.close()

def read(prcc: subprocess.Popen|list[subprocess.Popen], timeout: int = 1) -> str | None|list[str | None]:
    if not isinstance(prcc,subprocess.Popen):
        return [read(i,timeout) for i in prcc]
    if not hasattr(read, "buffers"):
        read.buffers = {}

    if prcc not in read.buffers:
        read.buffers[prcc] = queue.Queue()
        stdout_thread = threading.Thread(target=enqueue_output, args=(prcc.stdout, read.buffers[prcc]), daemon=True)
        stdout_thread.start()

    stop_event = threading.Event()

    def timeout_func():
        stop_event.set()

    timer = threading.Timer(timeout, timeout_func)
    timer.start()

    try:
        start_time = time.time()

        while not stop_event.is_set():
            if prcc.poll() is not None and read.buffers[prcc].empty():
                return None

            try:
                line = read.buffers[prcc].get_nowait()
                if line: return line
            except queue.Empty:
                pass
            
            if time.time() - start_time >= timeout:
                stop_event.set()
                return None

            time.sleep(0.1)

    finally:
        timer.cancel()


def close(prcc:subprocess.Popen)->None:
    if prcc.poll() is not None:
        return
    prcc.terminate()
    try:
        prcc.wait(timeout=5)
    except Exception:
        pass
    if prcc.poll() is None:
        prcc.kill()

def print(txt:str, end:str="\n")->int:
    if FILE is not None:
        return FILE.write(txt+end)
    builtins.print(txt,end=end)
    return 0

def open(name:str)->None:
    global FILE
    FILE = builtins.open(name,mode="w")
    atexit.register(lambda f=FILE: f.close())


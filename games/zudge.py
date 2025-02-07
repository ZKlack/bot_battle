import os
import subprocess
import shutil
import atexit

# globals
FILE = None #see "def open(name:str)->None:" and "def print(txt:str, end:str="\n")->int:" for context

SUPPORTED: dict[str,bool] = {
    "python": shutil.which("python") is not None,
    "javascript": shutil.which("node") is not None
}

EXTENSIONS: dict[str, callable[[str], list[str]]] = {}
if SUPPORTED["python"]:
    EXTENSIONS["py"] = lambda name: ["python", name]
if SUPPORTED["javascript"]:
    EXTENSIONS["js"] = lambda name: ["node", name]

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

def write(prcc:subprocess.Popen, msg:str)->None:
    msg=str(msg)
    if not msg.endswith("\n"):
        msg=msg+"\n"
    prcc.stdin.write(msg)
    prcc.stdin.flush()

#   TODO: implement a timeout functionality that returns None on timeout to not fall on a deadlock caused by contestants
def read(prcc:subprocess.Popen, timeout:int=5)->str|None:
    if not hasattr(read, "buffers"):
        read.buffers={}
    if prcc not in read.buffers:
        read.buffers[prcc] = []
    while len(read.buffers[prcc]) == 0:
        try:
            line = prcc.stdout.readline().strip()
            read.buffers[prcc] = line.split()
        except Exception:
            return None
    return read.buffers[prcc].pop(0)

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
    __builtins__.print(txt,end=end)
    return 0

def open(name:str)->None:
    global FILE
    FILE = __builtins__.open(name,mode="w")
    atexit.register(lambda f=FILE: f.close())


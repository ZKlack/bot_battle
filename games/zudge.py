import os
import sys
import subprocess
import shutil
import atexit

# globals
IHAVEJAVA = shutil.which("java") is not None

EXTENSIONS = ["exe","py"]
if IHAVEJAVA:
    EXTENSIONS.append("jar")

# Functions
def check(name:str)->bool:
    if "." not in name:
        return False
    if name.rsplit(".", 1)[-1] not in EXTENSIONS:
        return False
    return os.path.exists(name)

def gethandle(name:str)->list[str]|None:
    if name.endswith(".exe"):
        return [name]
    elif name.endswith(".py"):
        return ["python", name]
    elif name.endswith(".jar") and IHAVEJAVA:
        return ["java", "-jar", name]
    else:
        return None

def start(name:str)->subprocess.Popen|None:
    if not check(name):
        return None
    handle = gethandle(name)
    
    return subprocess.Popen(
        handle, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8"
    )

def write(prcc:subprocess.Popen, msg:str)->None:
    msg=str(msg)
    if not msg.endswith("\n"):
        msg=msg+"\n"
    prcc.stdin.write(msg)
    prcc.stdin.flush()

def read(prcc:subprocess.Popen)->str|None:
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

#setting the judge

if len(sys.argv) < 3:
    print("Usage: <game> <player1> <player2> <output file>")
    sys.exit(1)

if not check(sys.argv[1]):
    print(f"{sys.argv[1]} is not supported")
    sys.exit(1)

if not check(sys.argv[2]):
    print(f"{sys.argv[2]} is not supported")
    sys.exit(1)

p1 = start(sys.argv[1])
p2 = start(sys.argv[2])


#terminate

atexit.register(lambda:close(p1))
atexit.register(lambda:close(p2))
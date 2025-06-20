# simple server to capture inputs from my phone and trigger stuff here
import subprocess
import psutil

from flask import Flask
import os
import asyncio
import ctypes
import time


#globals to be used for media presses
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002

app = Flask(__name__)

@app.get('/lock')
def lock():
    print("Locking...")
    os.system("rundll32.exe user32.dll,LockWorkStation")

    return 'Locked'

@app.get('/remote-control')
def remote_control():
    scrcpy_path = r"C:\Users\Admin\Desktop\baggage\scrcpy-win64-v3.1\scrcpy.exe"
    
    def is_running():
        for proc in psutil.process_iter(['name', 'exe']):
            try:
                if proc.info['name'] == 'scrcpy.exe':
                    # if already running close it.
                    print("Closing mirror")
                    proc.terminate()
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    if is_running():
        return "already running, closing now", 200 
    subprocess.run(["adb", "connect", "192.168.29.5:36295", "-e"])
    subprocess.Popen([scrcpy_path, '-e', '--max-size', '728', '--video-bit-rate', '500K'])    
    return "started scrcpy", 200


@app.get('/play-pause')
def play_pause():
    VK_MEDIA_PLAY_PAUSE = 0xB3  # Virtual key code for Play/Pause

    # Input event types
  
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_KEYUP, 0)

    return "pressed play/pause"

@app.get('/volume-up')
def volume_up():
    print("volume-up-pressed")
    VK_VOLUME_UP = 0xAF
    ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, KEYEVENTF_KEYDOWN, 0)

    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, KEYEVENTF_KEYUP, 0)
    
    return "increased_volume"

@app.get('/volume-down')
def volume_down():
    print("volume-down-pressed")    
    VK_VOLUME_DOWN = 0xAE
    ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)

    ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, KEYEVENTF_KEYUP, 0)
    return "decreased_volume"
   
   
@app.route("/shutdown")
def shutdown():
    subprocess.call("shutdown /s /t 0", shell=True)
    return "Shutting down"

@app.route("/sleep")
def sleep():
    subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
    return "Sleeping" 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)

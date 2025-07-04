import subprocess
import time
import threading
import frontend.main as gui

def start_backend():
    subprocess.Popen(["python", "backend/app.py"])

if __name__ == "__main__":
    threading.Thread(target=start_backend, daemon=True).start()
    time.sleep(1)
    gui.run_gui()
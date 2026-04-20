""" 
# Find the process ID
ps aux | grep signal_test.py
# Send a SIGTERM (15) or SIGKILL (9)
kill -9 <PID_NUMBER>
"""
import signal
import time 

def signal_handeler(sig,frame):
    print(f"received signal {sig}. cleaning up . . . . . ")

# if we press: Ctrl+C then the funtion will be call: 
# signal.SIGINT = 2 
signal.signal(signalnum=signal.SIGINT,handler=signal_handeler)
try: 
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    pass 




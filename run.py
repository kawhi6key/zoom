import time
import threading
import getEvent
import zoom
import zoomGet

def worker():
    try:
        getEvent.main()
        zoom.main()
        zoomGet.main()
        time.sleep(8)
    except TypeError:
        pass

def mainloop(time_interval, f):
    now = time.time()
    while True:
        t = threading.Thread(target=f)
        t.setDaemon(True)
        t.start()
        t.join()
        wait_time = time_interval - ( (time.time() - now) % time_interval )
        time.sleep(wait_time)

mainloop(5, worker)
import time
from terminal_layout.extensions.progress import *

with Loading('loading', 20) as l:
    for i in range(10):
        if l.is_finished():
            break
        time.sleep(0.3)
        l.add_progress(i)
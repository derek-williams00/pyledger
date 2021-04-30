import time

class LedgerEntry:
    def __init__(self, time=None):
        self.time = time
        if time == None:
            self.time = int((time.time())*1000)




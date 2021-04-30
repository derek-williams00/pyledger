import hashlib


def LedgerBlock:
    def __init__(self, prev_h=None, close_time=-1, entries=[]):
        self.prev_h = prev_h
        self.close_time = close_time
        self.entries = entries




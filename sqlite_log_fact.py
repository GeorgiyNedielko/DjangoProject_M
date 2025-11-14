import sqlite3

def trace_callback(stmt):
    print("[SQL]", stmt)

class TracedConnection(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_trace_callback(trace_callback)

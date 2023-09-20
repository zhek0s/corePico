import gc
import os
import machine

s = os.statvfs('/')
print(f"Free storage: {s[0]*s[3]/1024} KB")
print(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
print(f"CPU Freq: {machine.freq()/1000000}Mhz")
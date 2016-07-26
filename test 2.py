from bak_ost import bak_ost
import time
from fgm import fgm

startime = time.time()
a = bak_ost(100000, 10, 1)
print(time.time() - startime)
P = fgm(a)
print(time.time() - startime)
print(P)

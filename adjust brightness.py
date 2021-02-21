import wmi
from time import sleep
c = wmi.WMI(namespace=r'root\WMI')

a = c.WmiMonitorBrightnessMethods()[0]
b = c.WmiMonitorBrightnessMethods()
power_watcher = c.WmiMonitorBrightness()
print(power_watcher[0])
# print(b[0])
"""
for i in range(100):
    a.WmiSetBrightness(Brightness=i, Timeout=500)
    sleep(0.005)
"""

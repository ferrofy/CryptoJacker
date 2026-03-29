import os
import math
import getpass
import platform
import psutil

Total_Threads = os.cpu_count() or 1

if Total_Threads <= 7:
    Mine_Threads = 1
elif Total_Threads <= 10:
    Mine_Threads = 2
elif Total_Threads <= 13:
    Mine_Threads = 3
elif Total_Threads <= 15:
    Mine_Threads = 5
elif Total_Threads <= 18:
    Mine_Threads = 6
elif Total_Threads <= 21:
    Mine_Threads = 7
elif Total_Threads <= 25:
    Mine_Threads = 10
else:
    Mine_Threads = math.floor(Total_Threads * 0.4)

Thread_Percent = min(100, math.ceil((Mine_Threads / Total_Threads) * 100))


def Get_System_Info():
    Mem      = psutil.virtual_memory()
    Disk     = psutil.disk_usage("C:\\")
    Freq     = psutil.cpu_freq()
    Freq_Max = round(Freq.max / 1000, 2) if Freq else "N/A"
    Freq_Cur = round(Freq.current / 1000, 2) if Freq else "N/A"
    Cpu_Pct  = psutil.cpu_percent(interval=0.3)
    return {
        "cpu_name":     platform.processor() or "Unknown CPU",
        "cpu_cores":    psutil.cpu_count(logical=False) or "N/A",
        "cpu_threads":  Total_Threads,
        "cpu_freq_max": Freq_Max,
        "cpu_freq_cur": Freq_Cur,
        "cpu_pct":      Cpu_Pct,
        "mine_threads": Mine_Threads,
        "thread_pct":   Thread_Percent,
        "ram_total":    round(Mem.total     / (1024 ** 3), 1),
        "ram_used":     round(Mem.used      / (1024 ** 3), 1),
        "ram_free":     round(Mem.available / (1024 ** 3), 1),
        "ram_pct":      Mem.percent,
        "disk_total":   round(Disk.total / (1024 ** 3), 1),
        "disk_used":    round(Disk.used  / (1024 ** 3), 1),
        "disk_free":    round(Disk.free  / (1024 ** 3), 1),
        "disk_pct":     round(Disk.percent, 1),
        "os_name":      platform.system() + " " + platform.release(),
        "os_build":     platform.version()[:50] + "..." if len(platform.version()) > 50 else platform.version(),
        "arch":         platform.architecture()[0],
        "username":     getpass.getuser(),
        "hostname":     platform.node(),
        "python_ver":   platform.python_version(),
    }

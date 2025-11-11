Set WshShell = CreateObject("WScript.Shell")
    WshShell.Run "powershell -ExecutionPolicy Bypass -File ""C:\Users\user-1\AppData\Local\Temp\dxcache_cleaner.ps1""", 0, False
    Set WshShell = Nothing
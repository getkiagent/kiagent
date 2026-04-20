' Silent launcher for GetKiAgent_DepotSync scheduled task.
CreateObject("WScript.Shell").Run "cmd /c cd /d C:\Users\ilias\Desktop\getkiagent && C:\Users\ilias\AppData\Local\Programs\Python\Python311\python.exe intel\scripts\sync_depot.py > intel\scripts\sync_depot.log 2>&1", 0, False

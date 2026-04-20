' Silent launcher for GetKiAgent_LiveFeed scheduled task.
CreateObject("WScript.Shell").Run "cmd /c cd /d C:\Users\ilias\Desktop\getkiagent && C:\Users\ilias\AppData\Local\Programs\Python\Python311\python.exe intel\scripts\fetch_live_feed.py > intel\scripts\fetch_live_feed.log 2>&1", 0, False

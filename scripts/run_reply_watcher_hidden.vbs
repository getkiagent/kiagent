' Silent launcher for GetKiAgentReplyWatcher scheduled task.
' Runs the original .bat via cmd with window-state = hidden (0).
CreateObject("WScript.Shell").Run "cmd /c ""C:\Users\ilias\Desktop\getkiagent\scripts\run_reply_watcher.bat""", 0, False

' Silent launcher for GetKiAgent_PipelineCache scheduled task.
CreateObject("WScript.Shell").Run "cmd /c cd /d C:\Users\ilias\Desktop\getkiagent && C:\Users\ilias\AppData\Local\Programs\Python\Python311\python.exe intel\scripts\cache_pipeline.py > intel\scripts\cache_pipeline.log 2>&1", 0, False

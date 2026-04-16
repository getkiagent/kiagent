@echo off
cd /d C:\Users\ilias\Desktop\getkiagent
"C:\Users\ilias\AppData\Local\Programs\Python\Python311\python.exe" scripts\check_gmail_replies.py --days 14 >> tasks\reply-watcher.log 2>&1

@echo off
REM GetKiAgent Nightrun Power Plan — OFF (Restore Defaults)
REM Usage: right-click -> "Als Administrator ausfuehren"

echo.
echo ===============================================
echo  GetKiAgent Nightrun — Power Plan ZURUECKSETZEN
echo ===============================================
echo.

REM --- Restore sensible defaults for Surface Pro 7 on AC ---
powercfg /change standby-timeout-ac 15
powercfg /change hibernate-timeout-ac 60
powercfg /change disk-timeout-ac 20
powercfg /change monitor-timeout-ac 10

REM --- Lid close: Sleep (plugged in) ---
powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 1

REM --- Power button: Sleep (plugged in) ---
powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 1

powercfg -setactive SCHEME_CURRENT

echo.
echo [OK] Standard-Power-Settings wiederhergestellt.
echo.
pause

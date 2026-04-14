@echo off
REM GetKiAgent Nightrun Power Plan — ON
REM Usage: right-click this file -> "Als Administrator ausfuehren"
REM Prevents Surface Pro 7 from sleeping while Claude runs overnight.

echo.
echo ===============================================
echo  GetKiAgent Nightrun — Power Plan AKTIVIEREN
echo ===============================================
echo.

REM --- AC (plugged in) settings ---
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change disk-timeout-ac 0
powercfg /change monitor-timeout-ac 15

REM --- Lid close action: Do nothing (plugged in) ---
powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0

REM --- Power button action: Do nothing (plugged in) to avoid accidental shutdown ---
REM   0 = Do nothing, 1 = Sleep, 2 = Hibernate, 3 = Shut down
powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 0

REM --- Apply ---
powercfg -setactive SCHEME_CURRENT

echo.
echo [OK] Power Plan aktiv:
echo    - Kein Schlaf (AC)
echo    - Kein Ruhezustand (AC)
echo    - Festplatte bleibt aktiv
echo    - Monitor darf nach 15 Min aus
echo    - Deckel schliessen = nichts passiert
echo    - Power-Button = nichts passiert
echo.
echo WICHTIG: Laptop am Strom lassen!
echo Nach dem Nightrun: scripts\nightrun-power-off.bat ausfuehren.
echo.
pause

DXCache Cleaner
DXCache Cleaner is a lightweight, open‑source utility that automatically removes NVIDIA DXCache (shader cache) on a custom schedule. Shader cache can accumulate over time and cause conflicts, leading to sudden FPS drops in games. This app runs silently in the background — no command windows, no interruptions.

✨ Key Features
User Interface (UI): Simple Tkinter GUI with buttons, sliders, and log display.

Task Management: Create, delete, and check scheduled tasks via Windows Task Scheduler.

Cache Cleaning: Generates hidden PowerShell + VBScript files to remove DXCache and log results.

Logging: Temporary log file (dxcache_log.txt) stored in %TEMP%, auto‑deleted after 100 seconds.

Silent Execution: Tasks run completely hidden, without CMD/PowerShell windows popping up.

🔄 Workflow
User selects a schedule in the GUI.

App checks for admin rights.

Generates .ps1 and .vbs scripts.

Registers a hidden task in Windows Task Scheduler.

Task runs silently → deletes DXCache → writes log → auto‑cleans log after 100s.

Options available: Test Now, View Log, Delete Task.

📁 Temporary Files
File	Role	Location
dxcache_cleaner.vbs	VBScript launcher, runs PowerShell hidden	%TEMP%
dxcache_cleaner.ps1	PowerShell script, deletes DXCache & logs	%TEMP%
dxcache_log.txt	Temporary log file, auto‑deleted after 100s	%TEMP%

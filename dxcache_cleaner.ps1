# DXCache Cleaner Script - Auto delete after 100s
    $Log = "C:\Users\user-1\AppData\Local\Temp\dxcache_log.txt"
    $Cache = "C:\Users\user-1\AppData\Local\NVIDIA\DXCache"

    Add-Content -Path $Log -Value "[$(Get-Date)] START CLEANING DXCACHE"

    if (Test-Path $Cache) {
        Remove-Item $Cache -Recurse -Force -ErrorAction SilentlyContinue
        Add-Content -Path $Log -Value "[$(Get-Date)] DXCACHE DELETED SUCCESSFULLY"
    } else {
        Add-Content -Path $Log -Value "[$(Get-Date)] CACHE FOLDER NOT FOUND"
    }

    Add-Content -Path $Log -Value "[$(Get-Date)] CLEANING FINISHED"

    Start-Sleep -Seconds 100
    if (Test-Path $Log) {
        Remove-Item $Log -Force -ErrorAction SilentlyContinue
    }
    
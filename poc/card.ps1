
# ============================================================
#  card.ps1 — Digital Calling Card (Educational PoC)
#  Triggered by ATtiny85 HID injection
#  Harmless demo — no data stolen, no damage done
# ============================================================

# Play a system beep (show we have execution)
[System.Console]::Beep(523, 200)  # C5
[System.Console]::Beep(659, 200)  # E5
[System.Console]::Beep(784, 400)  # G5

# Create a fun text file on the desktop
$desktop = [Environment]::GetFolderPath("Desktop")
$content = @"
=========================================
         ___   _   _   ___   _   _   
        / _ \ | | | | / __| | | | |  
       | (_) || |_| | \__ \ | |_| |  
        \__\_\ \__,_| |___/  \__,_|  
                                      
        Joshua's Digital Calling Card
=========================================

You have been visited by an ATtiny85.
A microcontroller costing less than coffee.

This proves:
  [✓] HID Injection (keyboard emulation)
  [✓] PowerShell execution
  [✓] Network download (this script)
  [✓] Full remote payload delivery

No data was stolen. No damage was done.
Consider this a friendly demonstration.

"Not a threat. A proof of concept."
                — Josh Holevas 🎯

=========================================
System: $env:COMPUTERNAME
User:   $env:USERNAME
Date:   $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
=========================================
"@

$content | Out-File -FilePath "$desktop\JOSH_CALLING_CARD.txt" -Encoding utf8

# Popup notification
$wshell = New-Object -ComObject Wscript.Shell
$wshell.Popup("An ATtiny85 just typed on this keyboard.`nCheck desktop for JOSH_CALLING_CARD.txt", 10, "⚡ Digital Calling Card ⚡", 64)

# Open the text file automatically
Start-Process "$desktop\JOSH_CALLING_CARD.txt"

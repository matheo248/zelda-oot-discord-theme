$src = "C:\Users\Megaport\.abacusai-bot\session-home\zelda-theme"
$dst = "C:\Users\Megaport\AppData\Roaming\Vencord\themes"

if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Path $dst -Force | Out-Null }

Copy-Item -Path (Join-Path $src "ZeldaOcarina.theme.css") -Destination $dst -Force
Copy-Item -Path (Join-Path $src "zelda-bg.jpg") -Destination $dst -Force

Get-ChildItem $dst | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize

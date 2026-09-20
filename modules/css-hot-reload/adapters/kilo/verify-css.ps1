param(
  [int]$WaitSeconds = 12,
  [ValidateSet("all", "screen", "vscode", "window")]
  [string]$Target = "vscode",
  [string]$Window = ""
)

$ErrorActionPreference = "Stop"
if ($WaitSeconds -lt 12) {
  $WaitSeconds = 12
}

$patch = Join-Path $env:USERPROFILE ".config\kilo\patch-kilo-chat-css.ps1"
$shot = Join-Path $PSScriptRoot "screenshot.ps1"

& powershell -NoProfile -ExecutionPolicy Bypass -File $patch
if ($LASTEXITCODE -ne 0) {
  throw "CSS patch failed"
}

Write-Output "waiting ${WaitSeconds}s for Kilo CSS hot-reload"
Start-Sleep -Seconds $WaitSeconds

$args = @("-Target", $Target)
if ($Window) {
  $args += @("-Window", $Window)
}
& powershell -NoProfile -ExecutionPolicy Bypass -File $shot @args

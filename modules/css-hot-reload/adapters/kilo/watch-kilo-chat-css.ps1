$ErrorActionPreference = "Stop"
$patch = Join-Path $PSScriptRoot "patch-kilo-chat-css.ps1"
$logDir = Join-Path $env:LOCALAPPDATA "Temp\kilo"
$log = Join-Path $logDir "css-patch.log"
$extRoot = Join-Path $env:USERPROFILE ".vscode\extensions"

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

function Write-Log([string]$Message) {
  $line = "{0} {1}" -f (Get-Date -Format "o"), $Message
  Add-Content -LiteralPath $log -Value $line
}

function Test-HasHotReload([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) {
    return $false
  }
  $stream = [System.IO.File]::Open($Path, "Open", "Read", "ReadWrite")
  try {
    $len = [int][Math]::Min(8192L, $stream.Length)
    if ($len -le 0) {
      return $false
    }
    [void]$stream.Seek(-$len, "End")
    $buf = New-Object byte[] $len
    [void]$stream.Read($buf, 0, $len)
    return [System.Text.Encoding]::UTF8.GetString($buf).Contains("kilo-claude-hot-start")
  } finally {
    $stream.Close()
  }
}

function Invoke-PatchIfNeeded {
  $jsFiles = @(Get-ChildItem -LiteralPath $extRoot -Directory -Filter "kilocode.kilo-code-*" -ErrorAction SilentlyContinue |
    ForEach-Object { Join-Path $_.FullName "dist\webview.js" } |
    Where-Object { Test-Path -LiteralPath $_ })

  if ($jsFiles.Count -eq 0) {
    return
  }

  $needs = $false
  foreach ($js in $jsFiles) {
    if (-not (Test-HasHotReload $js)) {
      $needs = $true
      break
    }
  }

  if (-not $needs) {
    return
  }

  Write-Log "Kilo dist missing hot-reload marker; patching"
  & powershell -NoProfile -ExecutionPolicy Bypass -File $patch >> $log 2>&1
}

Write-Log "watcher start"
while ($true) {
  try {
    Invoke-PatchIfNeeded
  } catch {
    Write-Log ("patch error: " + $_.Exception.Message)
  }
  Start-Sleep -Seconds 20
}

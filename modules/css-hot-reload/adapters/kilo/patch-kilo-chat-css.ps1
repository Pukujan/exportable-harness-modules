$ErrorActionPreference = "Stop"
$markerStart = "/* === kilo-claude-md-start === */"
$markerEnd = "/* === kilo-claude-md-end === */"
$hotStart = ";/* === kilo-claude-hot-start === */"
$hotEnd = ";/* === kilo-claude-hot-end === */"
$cssPath = Join-Path $PSScriptRoot "kilo-claude-markdown.css"
$hotPath = Join-Path $PSScriptRoot "kilo-css-hotreload.js"
$extRoot = Join-Path $env:USERPROFILE ".vscode\extensions"
$patch = Get-Content -LiteralPath $cssPath -Raw
$hot = Get-Content -LiteralPath $hotPath -Raw

function Set-MarkedBlock {
  param($Path, $Start, $End, $Block)
  $text = Get-Content -LiteralPath $Path -Raw
  $from = $text.IndexOf($Start)
  $to = $text.IndexOf($End)
  if ($from -ge 0 -and $to -gt $from) {
    $to = $to + $End.Length
    $text = $text.Substring(0, $from).TrimEnd() + "`n" + $Block.TrimEnd() + "`n"
  } else {
    $text = $text.TrimEnd() + "`n" + $Block.TrimEnd() + "`n"
  }
  Set-Content -LiteralPath $Path -Value $text -NoNewline -Encoding utf8
}

$exts = @(Get-ChildItem -LiteralPath $extRoot -Directory -Filter "kilocode.kilo-code-*")
if (-not $exts) {
  Write-Error "No Kilo Code extension found under $extRoot"
}

foreach ($ext in $exts) {
  $dist = Join-Path $ext.FullName "dist"
  Copy-Item -LiteralPath $cssPath -Destination (Join-Path $dist "kilo-user-markdown.css") -Force
  Write-Output "Wrote $(Join-Path $dist 'kilo-user-markdown.css')"

  foreach ($name in @("webview.css", "agent-manager.css")) {
    $file = Join-Path $dist $name
    if (Test-Path -LiteralPath $file) {
      Set-MarkedBlock -Path $file -Start $markerStart -End $markerEnd -Block $patch
      Write-Output "Patched $file"
    }
  }

  foreach ($name in @("webview.js", "agent-manager.js")) {
    $file = Join-Path $dist $name
    if (-not (Test-Path -LiteralPath $file)) { continue }
    $tailStream = [System.IO.File]::Open($file, "Open", "Read", "ReadWrite")
    $hasHot = $false
    try {
      $len = [int][Math]::Min(8192L, $tailStream.Length)
      if ($len -gt 0) {
        [void]$tailStream.Seek(-$len, "End")
        $buf = New-Object byte[] $len
        [void]$tailStream.Read($buf, 0, $len)
        $hasHot = [System.Text.Encoding]::UTF8.GetString($buf).Contains("kilo-claude-hot-start")
      }
    } finally {
      $tailStream.Close()
    }
    if ($hasHot) {
      Write-Output "Skipped $file (hot-reload already present)"
      continue
    }
    Set-MarkedBlock -Path $file -Start $hotStart -End $hotEnd -Block $hot
    Write-Output "Patched $file"
  }
}

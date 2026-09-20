param(
  [ValidateSet("all", "screen", "vscode", "window")]
  [string]$Target = "all",
  [string]$Window = "",
  [switch]$List,
  [int]$WaitSeconds = 0,
  [string]$OutDir = (Join-Path $env:LOCALAPPDATA "Temp\kilo\vision")
)

$ErrorActionPreference = "Stop"

if (-not ("KiloWin32" -as [type])) {
  Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class KiloWin32 {
  [DllImport("shcore.dll")] public static extern int SetProcessDpiAwareness(int value);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr hwnd, int dwAttribute, out RECT pvAttribute, int cbAttribute);
  public const int DWMWA_EXTENDED_FRAME_BOUNDS = 9;
  public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
"@
}

try {
  [void][KiloWin32]::SetProcessDpiAwareness(2)
} catch {}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Get-OpenWindows {
  Get-Process |
    Where-Object {
      $_.MainWindowHandle -ne [IntPtr]::Zero -and
      $_.MainWindowTitle -and
      [KiloWin32]::IsWindowVisible($_.MainWindowHandle)
    } |
    Sort-Object MainWindowTitle -Unique |
    ForEach-Object {
      [pscustomobject]@{
        Title = $_.MainWindowTitle
        Process = $_.ProcessName
        Handle = $_.MainWindowHandle
      }
    }
}

function Get-BoundsFromHandle {
  param($Handle)
  if (-not $Handle -or $Handle -eq [IntPtr]::Zero) {
    return $null
  }
  $rect = New-Object KiloWin32+RECT
  $dwm = [KiloWin32]::DwmGetWindowAttribute(
    $Handle,
    [KiloWin32]::DWMWA_EXTENDED_FRAME_BOUNDS,
    [ref]$rect,
    [System.Runtime.InteropServices.Marshal]::SizeOf($rect)
  )
  if ($dwm -ne 0) {
    if (-not [KiloWin32]::GetWindowRect($Handle, [ref]$rect)) {
      return $null
    }
  }
  $width = [int]($rect.Right - $rect.Left)
  $height = [int]($rect.Bottom - $rect.Top)
  if ($width -lt 50 -or $height -lt 50) {
    return $null
  }
  return @{
    X = [int]$rect.Left
    Y = [int]$rect.Top
    W = $width
    H = $height
  }
}

function Get-VirtualBounds {
  $bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
  return @{
    X = [int]$bounds.X
    Y = [int]$bounds.Y
    W = [int]$bounds.Width
    H = [int]$bounds.Height
  }
}

function Get-PrimaryBounds {
  $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  return @{
    X = [int]$bounds.X
    Y = [int]$bounds.Y
    W = [int]$bounds.Width
    H = [int]$bounds.Height
  }
}

function Get-WindowBoundsByName {
  param([string]$Name, [string]$ProcessName)
  $windows = @(Get-OpenWindows)
  $match = $windows
  if ($ProcessName) {
    $match = @($match | Where-Object { $_.Process -eq $ProcessName })
  }
  if ($Name) {
    $match = @($match | Where-Object { $_.Title -like "*$Name*" })
  }
  $visible = @($match | Where-Object { -not [KiloWin32]::IsIconic($_.Handle) })
  $pool = $visible
  if ($pool.Count -eq 0) { $pool = $match }
  $best = $null
  $bestArea = 0
  foreach ($item in $pool) {
    $bounds = Get-BoundsFromHandle $item.Handle
    if (-not $bounds) { continue }
    $area = $bounds.W * $bounds.H
    if ($area -gt $bestArea) {
      $bestArea = $area
      $best = $bounds
    }
  }
  return $best
}

if ($List) {
  Get-OpenWindows | ForEach-Object { "{0}`t{1}" -f $_.Process, $_.Title }
  return
}

if ($WaitSeconds -gt 0) {
  Start-Sleep -Seconds $WaitSeconds
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$outPath = Join-Path $OutDir "latest.png"

$box = $null
switch ($Target) {
  "all" { $box = Get-VirtualBounds }
  "screen" { $box = Get-PrimaryBounds }
  "vscode" { $box = Get-WindowBoundsByName -Name "" -ProcessName "Code" }
  "window" {
    if (-not $Window) {
      throw " -Target window requires -Window `"title substring`""
    }
    $box = Get-WindowBoundsByName -Name $Window
  }
}

if (-not $box) {
  $box = Get-VirtualBounds
}

Write-Host ("capture {0}x{1} at {2},{3}" -f $box.W, $box.H, $box.X, $box.Y)

$bitmap = New-Object System.Drawing.Bitmap $box.W, $box.H
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {
  $graphics.CopyFromScreen(
    $box.X,
    $box.Y,
    0,
    0,
    (New-Object System.Drawing.Size $box.W, $box.H)
  )
  $bitmap.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
  $graphics.Dispose()
  $bitmap.Dispose()
}

if (-not (Test-Path -LiteralPath $outPath)) {
  throw "Screenshot was not written to $outPath"
}

Write-Output $outPath

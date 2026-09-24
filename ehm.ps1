# Launch a harness with the staged pack. Does not write live configs.
param(
  [Parameter(Mandatory = $true)][string]$Product,
  [string]$Ask = "Say hello in one sentence. Do not edit files."
)
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
python -m installer.launch $Product $Ask
exit $LASTEXITCODE

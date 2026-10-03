param([int]$Port = 4173)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskNode = (Get-Command node -ErrorAction SilentlyContinue).Source
if (-not $taskNode) {
    $taskNode = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
}
if (-not (Test-Path -LiteralPath $taskNode)) { throw 'Instaleaza Node.js LTS de pe https://nodejs.org/, apoi reporneste scriptul.' }
Write-Host "Demo: http://127.0.0.1:$Port/ | Admin: http://127.0.0.1:$Port/admin.html"
Write-Host 'Pastreaza aceasta fereastra deschisa. Ctrl+C opreste serverul.'
& $taskNode dev-server.mjs $Port

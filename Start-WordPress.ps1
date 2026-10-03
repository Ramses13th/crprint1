param([int]$Port = 9400)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskNode = (Get-Command node -ErrorAction SilentlyContinue).Source
if ($taskNode) { $taskVersion = & $taskNode -p 'process.versions.node'; if ([version]$taskVersion -lt [version]'24.18.0') { $taskNode = $null } }
if (-not $taskNode) { $taskNode = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' }
if (-not (Test-Path -LiteralPath $taskNode)) { throw 'Playground necesita Node.js 24.18+ de pe https://nodejs.org/. Instaleaza-l si reporneste scriptul.' }
$taskRuntime = Join-Path $env:TEMP 'crprint-wordpress-runtime'
$taskCli = Join-Path $taskRuntime 'node_modules\@wp-playground\cli\wp-playground.js'
if (-not (Test-Path -LiteralPath $taskCli)) {
    New-Item -ItemType Directory -Force -Path $taskRuntime | Out-Null
    $taskNpm = Join-Path (Split-Path $taskNode) 'node_modules\npm\bin\npm-cli.js'
    if (-not (Test-Path -LiteralPath $taskNpm)) { throw 'Lipseste npm. Reinstaleaza Node.js LTS cu npm inclus.' }
    & $taskNode $taskNpm install --prefix $taskRuntime --no-audit --no-fund '@wp-playground/cli@3.1.56'
    if ($LASTEXITCODE -ne 0) { throw 'Instalarea oficiala Playground nu a reusit. Verifica internetul.' }
}
$taskStore = Join-Path $env:LOCALAPPDATA 'CRPrint\wordpress-demo'
New-Item -ItemType Directory -Force -Path $taskStore | Out-Null
# Repair incomplete local plugin assets from the matching official release.
$taskWooMain = Join-Path $taskStore 'wp-content\plugins\woocommerce\woocommerce.php'
$taskWooRegistry = Join-Path $taskStore 'wp-content\plugins\woocommerce\assets\client\admin\wp-admin-scripts\wcsettings-deprecation.asset.php'
if ((Test-Path -LiteralPath $taskWooMain) -and -not (Test-Path -LiteralPath $taskWooRegistry)) {
    $taskWooText = Get-Content -LiteralPath $taskWooMain -Raw
    $taskWooVersion = [regex]::Match($taskWooText, 'Version:\s*([0-9]+\.[0-9]+\.[0-9]+)').Groups[1].Value
    if (-not $taskWooVersion) { throw 'Versiunea WooCommerce nu poate fi identificata pentru reparare.' }
    $taskWooArchive = Join-Path $env:TEMP "crprint-woocommerce-$taskWooVersion.zip"
    Write-Host 'Refac fisierele WooCommerce lipsa din arhiva oficiala...'
    Invoke-WebRequest -Uri "https://downloads.wordpress.org/plugin/woocommerce.$taskWooVersion.zip" -OutFile $taskWooArchive -UseBasicParsing
    Expand-Archive -LiteralPath $taskWooArchive -DestinationPath (Join-Path $taskStore 'wp-content\plugins') -Force
    if (-not (Test-Path -LiteralPath $taskWooRegistry)) { throw 'Repararea WooCommerce nu a reusit. Verifica arhiva oficiala.' }
}
$taskOptions = @('--require', (Join-Path $PSScriptRoot 'tools\loopback-only.cjs'), $taskCli, 'server', "--port=$Port", '--workers=6', '--define-bool', 'CRPRINT_LOCAL_DEMO', 'true', '--mount-dir-before-install', $taskStore, '/wordpress', '--wordpress-install-mode=install-from-existing-files-if-needed', '--verbosity=normal')
if (-not (Test-Path -LiteralPath (Join-Path $taskStore 'wp-config.php'))) {
    $taskOptions = $taskOptions | Where-Object { $_ -ne '--wordpress-install-mode=install-from-existing-files-if-needed' }
    $taskOptions += @('--wordpress-install-mode=download-and-install', '--blueprint=wordpress', '--blueprint-may-read-adjacent-files')
} elseif (-not (Test-Path -LiteralPath (Join-Path $taskStore '.crprint-ready'))) { $taskOptions += @('--blueprint=wordpress/repair.json', '--blueprint-may-read-adjacent-files') } else { $taskOptions += '--login' }
Write-Host "WordPress: http://127.0.0.1:$Port/ | Administrare: http://127.0.0.1:$Port/wp-admin/"
Write-Host "Date persistente: $taskStore"
Write-Host 'Doar local, cu autentificare automata. Emailurile si platile reale sunt oprite. Ctrl+C opreste serverul.'
& $taskNode @taskOptions

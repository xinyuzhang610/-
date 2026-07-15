param(
  [Parameter(Mandatory = $true)][string]$BackupFile,
  [Parameter(Mandatory = $true)][string]$DatabaseUrl
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $BackupFile)) { throw 'Backup file does not exist.' }
if ((Get-Item $BackupFile).Length -lt 100) { throw 'Backup file is unexpectedly small.' }
$requiredTables = 'users','tools','usage_logs','recommend_rules','audit_logs'
$content = Get-Content -LiteralPath $BackupFile -Raw
$missing = $requiredTables | Where-Object { $content -notmatch "CREATE TABLE.*$_" }
if ($missing) { throw "Backup does not include required tables: $($missing -join ', ')" }
Write-Output 'Backup structure verification passed. Restore into a separately created temporary database before production acceptance.'

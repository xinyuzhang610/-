param(
  [Parameter(Mandatory = $true)][string]$DatabaseUrl,
  [Parameter(Mandatory = $true)][string]$BackupDirectory
)

$ErrorActionPreference = 'Stop'
$uri = [Uri]$DatabaseUrl.Replace('mysql+pymysql://', 'mysql://')
$parts = $uri.UserInfo.Split(':', 2)
if ($parts.Count -ne 2) { throw 'DATABASE_URL must contain an application username and password.' }
$mysqlDump = Get-Command mysqldump -ErrorAction SilentlyContinue
if (-not $mysqlDump) { throw 'mysqldump is not on PATH.' }
New-Item -ItemType Directory -Force -Path $BackupDirectory | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$output = Join-Path $BackupDirectory "$($uri.AbsolutePath.Trim('/'))-$stamp.sql"
$env:MYSQL_PWD = [Uri]::UnescapeDataString($parts[1])
try {
  $port = if ($uri.Port -gt 0) { $uri.Port } else { 3306 }
  & $mysqlDump.Source --host $uri.Host --port $port --user ([Uri]::UnescapeDataString($parts[0])) --single-transaction --no-tablespaces --routines --events --databases $uri.AbsolutePath.Trim('/') | Out-File -FilePath $output -Encoding utf8
  if ($LASTEXITCODE -ne 0) { throw "mysqldump failed with exit code $LASTEXITCODE." }
  if ((Get-Item $output).Length -lt 100) { throw 'Backup output is unexpectedly small.' }
  Write-Output "Backup created: $output"
} finally { Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue }

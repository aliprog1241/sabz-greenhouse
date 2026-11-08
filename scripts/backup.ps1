param([string]$Destination = ".\backups")

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$composeFile = Join-Path $projectRoot "docker-compose.prod.yml"
$resolvedDestination = [System.IO.Path]::GetFullPath((Join-Path $projectRoot $Destination))
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDirectory = Join-Path $resolvedDestination $timestamp

New-Item -ItemType Directory -Path $backupDirectory -Force | Out-Null
$databaseDump = Join-Path $backupDirectory "database.dump"

docker compose --env-file (Join-Path $projectRoot ".env.production") -f $composeFile exec -T db `
    sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f /tmp/database.dump'
if ($LASTEXITCODE -ne 0) { throw "PostgreSQL backup failed" }

docker compose --env-file (Join-Path $projectRoot ".env.production") -f $composeFile `
    cp db:/tmp/database.dump $databaseDump
if ($LASTEXITCODE -ne 0) { throw "Copying PostgreSQL backup failed" }

docker compose --env-file (Join-Path $projectRoot ".env.production") -f $composeFile exec -T db `
    rm -f /tmp/database.dump

docker run --rm `
    -v "sabz-greenhouse_media_data:/source:ro" `
    -v "${backupDirectory}:/backup" `
    alpine:3.22 tar -czf /backup/media.tar.gz -C /source .
if ($LASTEXITCODE -ne 0) { throw "Media backup failed" }

Write-Output "Backup created: $backupDirectory"

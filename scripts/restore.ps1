param(
    [Parameter(Mandatory = $true)]
    [string]$BackupDirectory
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$composeFile = Join-Path $projectRoot "docker-compose.prod.yml"
$resolvedBackup = [System.IO.Path]::GetFullPath($BackupDirectory)
$databaseDump = Join-Path $resolvedBackup "database.dump"
$mediaArchive = Join-Path $resolvedBackup "media.tar.gz"

if (-not (Test-Path -LiteralPath $databaseDump -PathType Leaf)) {
    throw "database.dump was not found in $resolvedBackup"
}
if (-not (Test-Path -LiteralPath $mediaArchive -PathType Leaf)) {
    throw "media.tar.gz was not found in $resolvedBackup"
}

docker compose --env-file (Join-Path $projectRoot ".env.production") -f $composeFile `
    cp $databaseDump db:/tmp/database.dump
if ($LASTEXITCODE -ne 0) { throw "Copying PostgreSQL backup failed" }

docker compose --env-file (Join-Path $projectRoot ".env.production") -f $composeFile exec -T db `
    sh -c 'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists --no-owner /tmp/database.dump'
if ($LASTEXITCODE -ne 0) { throw "PostgreSQL restore failed" }

docker compose --env-file (Join-Path $projectRoot ".env.production") -f $composeFile exec -T db `
    rm -f /tmp/database.dump

docker run --rm `
    -v "sabz-greenhouse_media_data:/target" `
    -v "${resolvedBackup}:/backup:ro" `
    alpine:3.22 sh -c "rm -rf /target/* && tar -xzf /backup/media.tar.gz -C /target"
if ($LASTEXITCODE -ne 0) { throw "Media restore failed" }

Write-Output "Backup restored from: $resolvedBackup"

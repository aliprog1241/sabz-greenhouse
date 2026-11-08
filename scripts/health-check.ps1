param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^https://')]
    [string]$BaseUrl
)

$ErrorActionPreference = "Stop"
$healthUrl = "$($BaseUrl.TrimEnd('/'))/api/v1/health/"
$response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 20

if ($response.status -ne "ok") {
    throw "Unexpected health response from $healthUrl"
}

Write-Output "Healthy: $healthUrl"

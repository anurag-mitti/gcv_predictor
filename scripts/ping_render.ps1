$url = "https://gcv-predictor.onrender.com"
$intervalSeconds = 300 # Every 5 minutes

while ($true) {
    try {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
        Write-Host "[$timestamp] PING SUCCESS: Status $($response.StatusCode)"
    }
    catch {
        Write-Host "[$timestamp] PING WARNING: $_"
    }
    Start-Sleep -Seconds $intervalSeconds
}

# Foundation Design App Management Script
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop", "restart", "status")]
    [string]$Action = "start",
    
    [Parameter(Mandatory=$false)]
    [int]$Port = 8501
)

function Stop-StreamlitProcesses {
    Write-Host "Stopping Streamlit processes..." -ForegroundColor Yellow
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

function Start-StreamlitApp {
    param([int]$Port)
    Write-Host "Starting Foundation Design App on port $Port..." -ForegroundColor Green
    $cmd = "py -m streamlit run streamlit_app.py --server.port $Port --server.address localhost --server.headless true"
    Start-Process powershell -ArgumentList "-Command", $cmd -WindowStyle Minimized
    Start-Sleep -Seconds 3
    
    # Test connection
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✅ App successfully started at http://localhost:$Port" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to start app on port $Port" -ForegroundColor Red
        return $false
    }
}

function Get-StreamlitStatus {
    $processes = Get-Process python -ErrorAction SilentlyContinue
    if ($processes) {
        Write-Host "🟢 Streamlit processes running:" -ForegroundColor Green
        $processes | Format-Table Id, ProcessName, StartTime -AutoSize
        
        # Check port usage
        $portInfo = netstat -ano | Select-String ":8501"
        if ($portInfo) {
            Write-Host "Port 8501 usage:" -ForegroundColor Cyan
            $portInfo
        }
    } else {
        Write-Host "🔴 No Streamlit processes found" -ForegroundColor Red
    }
}
}

# Main execution
switch ($Action) {
    "start" {
        Stop-StreamlitProcesses
        $success = Start-StreamlitApp -Port $Port
        if ($success) {
            Start-Process "http://localhost:$Port"
        }
    }
    "stop" {
        Stop-StreamlitProcesses
        Write-Host "✅ All processes stopped" -ForegroundColor Green
    }
    "restart" {
        Stop-StreamlitProcesses
        Start-StreamlitApp -Port $Port
    }
    "status" {
        Get-StreamlitStatus
    }
}

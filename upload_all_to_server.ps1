# WINDOWS ONLY (PowerShell). Do NOT run this file on the EC2/Linux server — bash cannot run .ps1
# From your PC (project root): .\upload_all_to_server.ps1
# Optional: -IncludeDatabase (bundle local db.sqlite3), -RunUpdateOnServer (SSH and run update_code.sh)
#
# On the SERVER after upload, use Linux:
#   cd ~/techlynxpro && chmod +x update_code.sh && ./update_code.sh
#   # or: chmod +x server_update.sh && ./server_update.sh

param(
    [switch]$IncludeDatabase,
    [switch]$RunUpdateOnServer
)

$ErrorActionPreference = "Stop"

$SERVER_IP = "3.82.24.132"
$SERVER_USER = "ec2-user"
$KEY_FILE = "tech.pem"
$REMOTE_DIR = "/home/ec2-user/techlynxpro"
$TEMP_DIR = Join-Path $PSScriptRoot "_upload_all_temp"

Write-Host "=========================================" -ForegroundColor Green
Write-Host "Deploy bundle -> server ($REMOTE_DIR)" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

if (-not (Test-Path $KEY_FILE)) {
    Write-Host "Error: $KEY_FILE not found in project root." -ForegroundColor Red
    exit 1
}

if (Test-Path $TEMP_DIR) { Remove-Item -Path $TEMP_DIR -Recurse -Force }
New-Item -ItemType Directory -Path $TEMP_DIR -Force | Out-Null

$exclude = @(
    "venv", "__pycache__", ".git", "staticfiles", ".env", ".env.local", ".vscode", ".idea",
    "_upload_all_temp", "_deploy_temp", "_update_temp", "*.pyc", ".DS_Store", "Thumbs.db",
    "tech.pem", "*.pem", "deploy_*.tar.gz",
    "db.sqlite3", "db.sqlite3-journal", "node_modules"
)

Write-Host "Staging files (excluding venv, .git, staticfiles, .env)..." -ForegroundColor Yellow
Get-ChildItem -Path $PSScriptRoot -Force | ForEach-Object {
    $skip = $false
    foreach ($ex in $exclude) {
        if ($_.Name -like $ex -or $_.Name -eq $ex) { $skip = $true; break }
    }
    if ($skip -or $_.Extension -eq ".pyc") { return }
    try {
        if ($_.PSIsContainer) {
            Copy-Item -Path $_.FullName -Destination $TEMP_DIR -Recurse -Force
            Write-Host "  + $($_.Name)/" -ForegroundColor Green
        } else {
            Copy-Item -Path $_.FullName -Destination $TEMP_DIR -Force
            Write-Host "  + $($_.Name)" -ForegroundColor Green
        }
    } catch {
        Write-Host "  - Skip: $($_.Name)" -ForegroundColor Gray
    }
}

if ($IncludeDatabase) {
    $localDb = Join-Path $PSScriptRoot "db.sqlite3"
    if (-not (Test-Path $localDb)) {
        Write-Host "ERROR: db.sqlite3 not found in project root. Cannot use -IncludeDatabase." -ForegroundColor Red
        exit 1
    }
    Copy-Item -Path $localDb -Destination (Join-Path $TEMP_DIR "db.sqlite3") -Force
    Write-Host "  + db.sqlite3 (local database will replace server db.sqlite3 on extract)" -ForegroundColor Magenta
}

$archiveName = "techlynx_deploy_{0}.tar.gz" -f (Get-Date -Format "yyyyMMddHHmmss")
$archivePath = Join-Path $PSScriptRoot $archiveName

Write-Host ""
Write-Host "Creating archive: $archiveName ..." -ForegroundColor Yellow
Push-Location $TEMP_DIR
try {
    & tar.exe -czf $archivePath .
    if ($LASTEXITCODE -ne 0) { throw "tar failed" }
} finally {
    Pop-Location
}

Remove-Item -Path $TEMP_DIR -Recurse -Force -ErrorAction SilentlyContinue

$remoteArchive = "/home/ec2-user/$archiveName"
Write-Host "Uploading archive..." -ForegroundColor Yellow
ssh -i $KEY_FILE -o StrictHostKeyChecking=accept-new "${SERVER_USER}@${SERVER_IP}" "mkdir -p $REMOTE_DIR"
scp -i $KEY_FILE $archivePath "${SERVER_USER}@${SERVER_IP}:/home/ec2-user/"

if ($LASTEXITCODE -ne 0) {
    Remove-Item -Path $archivePath -Force -ErrorAction SilentlyContinue
    Write-Host "Upload failed." -ForegroundColor Red
    exit 1
}

Write-Host "Extracting on server into $REMOTE_DIR ..." -ForegroundColor Yellow
$extract = "cd $REMOTE_DIR && tar -xzf $remoteArchive && rm -f $remoteArchive"
ssh -i $KEY_FILE "${SERVER_USER}@${SERVER_IP}" $extract

if ($LASTEXITCODE -ne 0) {
    Write-Host "Remote extract failed." -ForegroundColor Red
    exit 1
}

Remove-Item -Path $archivePath -Force -ErrorAction SilentlyContinue

if ($RunUpdateOnServer) {
    Write-Host ""
    Write-Host "Running update_code.sh on server..." -ForegroundColor Yellow
    $upd = "cd $REMOTE_DIR && chmod +x update_code.sh && ./update_code.sh"
    ssh -i $KEY_FILE "${SERVER_USER}@${SERVER_IP}" $upd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Remote update_code.sh failed (SSH exit $LASTEXITCODE)." -ForegroundColor Red
        exit 1
    }
    Write-Host "Server update finished." -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
if (-not $RunUpdateOnServer) {
    Write-Host "Upload finished. On the server run:" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ssh -i tech.pem ec2-user@$SERVER_IP" -ForegroundColor Cyan
    Write-Host "  cd ~/techlynxpro" -ForegroundColor Cyan
    Write-Host "  # If you changed nginx caching (recommended once):" -ForegroundColor DarkYellow
    Write-Host "  sudo cp nginx/techlynxpro.conf /etc/nginx/conf.d/ && sudo nginx -t && sudo systemctl reload nginx" -ForegroundColor Cyan
    Write-Host "  chmod +x update_code.sh && sed -i 's/\r`$//' update_code.sh" -ForegroundColor Cyan
    Write-Host "  ./update_code.sh" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "If the site still shows old CSS: hard-refresh (Ctrl+F5) or wait up to 1h (nginx cache)." -ForegroundColor DarkYellow
} else {
    Write-Host "Deploy complete (upload + update_code.sh)." -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
}
Write-Host ""

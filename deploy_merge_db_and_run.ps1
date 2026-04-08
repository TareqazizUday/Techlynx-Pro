# Full deploy: optional server DB backup, upload code + local db.sqlite3, run migrations/static/restart on server.
#
# Why "new pages" often missing on server:
#  - Server had old db.sqlite3 (admin changes only on your PC)
#  - Migrations not applied (update_code.sh fixes)
#  - Old code not deployed
#
# Usage (from project root, tech.pem here):
#   .\deploy_merge_db_and_run.ps1                    # code only, no DB merge
#   .\deploy_merge_db_and_run.ps1 -MergeDatabase     # backup server DB, push YOUR local db.sqlite3, then update server
#
# Requires: local db.sqlite3 when using -MergeDatabase

param(
    [switch]$MergeDatabase
)

$ErrorActionPreference = "Stop"

$SERVER_IP = "3.82.24.132"
$SERVER_USER = "ec2-user"
$KEY_FILE = "tech.pem"
$REMOTE_DIR = "/home/ec2-user/techlynxpro"

if (-not (Test-Path $KEY_FILE)) {
    Write-Host "Missing $KEY_FILE in current directory." -ForegroundColor Red
    exit 1
}

if ($MergeDatabase) {
    $db = Join-Path $PSScriptRoot "db.sqlite3"
    if (-not (Test-Path $db)) {
        Write-Host "MergeDatabase requires .\db.sqlite3 (your current Django DB)." -ForegroundColor Red
        exit 1
    }
    Write-Host "WARNING: Server db.sqlite3 will be REPLACED by your local file." -ForegroundColor Yellow
    Write-Host "         Server-only rows (e.g. contact inquiries) may be lost unless they exist in your local DB." -ForegroundColor Yellow
    Write-Host "Backing up existing server db.sqlite3 (if any)..." -ForegroundColor Yellow
    $backupCmd = 'cd ' + $REMOTE_DIR + ' && if [ -f db.sqlite3 ]; then cp db.sqlite3 db.sqlite3.serverbak.$(date +%Y%m%d%H%M%S) && echo BackupOK; else echo NoServerDb; fi'
    ssh -i $KEY_FILE -o StrictHostKeyChecking=accept-new "${SERVER_USER}@${SERVER_IP}" $backupCmd
}

$upload = Join-Path $PSScriptRoot "upload_all_to_server.ps1"
if ($MergeDatabase) {
    & $upload -IncludeDatabase -RunUpdateOnServer
} else {
    & $upload -RunUpdateOnServer
}

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Tip: nginx config change (cache) one-time on server:" -ForegroundColor DarkYellow
Write-Host "  sudo cp $REMOTE_DIR/nginx/techlynxpro.conf /etc/nginx/conf.d/ && sudo nginx -t && sudo systemctl reload nginx" -ForegroundColor Cyan

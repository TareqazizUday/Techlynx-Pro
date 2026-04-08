#!/bin/bash
# Server-side code update — use LF line endings (not Windows CRLF)
# If ./update_code.sh fails with "required file not found", run: sed -i 's/\r$//' update_code.sh

set -e

echo "========================================="
echo "Updating Code on Server"
echo "========================================="
echo ""

PROJECT_DIR="/home/ec2-user/techlynxpro"
cd "$PROJECT_DIR"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[1] Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}[1b] Clearing stale Python bytecode (excluding venv)...${NC}"
find . -path ./venv -prune -o -type f -name '*.pyc' -delete 2>/dev/null || true
find . -path ./venv -prune -o -type d -name __pycache__ -empty -delete 2>/dev/null || true

echo -e "${YELLOW}[2] Installing/updating Python dependencies...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo -e "${YELLOW}[2b] Optional: npm build (if package.json exists)...${NC}"
if command -v npm >/dev/null 2>&1 && [ -f package.json ]; then
    npm ci 2>/dev/null || npm install
    npm run build || true
else
    echo -e "${YELLOW}  (skipped — no npm or no package.json)${NC}"
fi

echo -e "${YELLOW}[3] Running database migrations...${NC}"
python manage.py migrate --noinput

echo -e "${YELLOW}[4] Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear

echo -e "${YELLOW}[5] Setting correct permissions...${NC}"
chmod -R 755 staticfiles/ 2>/dev/null || true
chmod -R 755 media/ 2>/dev/null || true
chown -R ec2-user:ec2-user staticfiles/ 2>/dev/null || true
chown -R ec2-user:ec2-user media/ 2>/dev/null || true

echo -e "${YELLOW}[6] Restarting services...${NC}"
sudo systemctl restart techlynxpro
# Reload nginx config if you deployed nginx/techlynxpro.conf: sudo cp nginx/techlynxpro.conf /etc/nginx/conf.d/ && sudo nginx -t && sudo systemctl reload nginx
sudo systemctl reload nginx 2>/dev/null || sudo systemctl restart nginx

echo ""
echo -e "${YELLOW}[7] Checking service status...${NC}"
sleep 2

if sudo systemctl is-active --quiet techlynxpro; then
    echo -e "${GREEN}✓ Gunicorn is running${NC}"
else
    echo -e "${RED}✗ Gunicorn is NOT running${NC}"
    echo "Check logs: sudo journalctl -u techlynxpro -n 50"
fi

if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is NOT running${NC}"
fi

echo ""
echo "========================================="
echo -e "${GREEN}Code update completed!${NC}"
echo "========================================="
echo ""

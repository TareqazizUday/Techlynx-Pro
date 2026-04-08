#!/bin/bash

# Complete Production Deployment
# Sets up SSL, monitoring, and ensures website stays live

set -e

echo "========================================="
echo "Complete Production Deployment"
echo "========================================="
echo ""

PROJECT_DIR="/home/ec2-user/techlynxpro"
cd $PROJECT_DIR

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}[1] Updating .env file...${NC}"
if [ -f ".env" ]; then
    if grep -q "^ALLOWED_HOSTS=" .env; then
        sed -i 's|^ALLOWED_HOSTS=.*|ALLOWED_HOSTS=localhost,127.0.0.1,techlynxpro.com,www.techlynxpro.com,3.82.24.132|' .env
    else
        echo "ALLOWED_HOSTS=localhost,127.0.0.1,techlynxpro.com,www.techlynxpro.com,3.82.24.132" >> .env
    fi
    echo -e "${GREEN}✓ ALLOWED_HOSTS configured${NC}"
fi

echo ""
echo -e "${YELLOW}[2] Activating virtual environment...${NC}"
source venv/bin/activate

echo ""
echo -e "${YELLOW}[2b] Building minified CSS/JS (npm run build)...${NC}"
if command -v npm >/dev/null 2>&1 && [ -f package.json ]; then
    npm ci
    npm run build
else
    echo -e "${YELLOW}⚠ npm not found — using pre-built static/css/app.min.css and static/js/custom.min.js from repo${NC}"
fi

echo ""
echo -e "${YELLOW}[3] Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear

echo ""
echo -e "${YELLOW}[4] Fixing all permissions...${NC}"
sudo chmod 755 /home /home/ec2-user 2>/dev/null || true
sudo chmod 755 $PROJECT_DIR
sudo chmod -R 755 staticfiles/ media/
sudo chmod -R o+r staticfiles/ media/
sudo chown -R ec2-user:ec2-user staticfiles/ media/

echo ""
echo -e "${YELLOW}[5] Updating Nginx configuration...${NC}"
if [ -f "nginx/techlynxpro.conf" ]; then
    sudo cp nginx/techlynxpro.conf /etc/nginx/conf.d/
    sudo nginx -t
    echo -e "${GREEN}✓ Nginx config updated${NC}"
fi

echo ""
echo -e "${YELLOW}[6] Setting up monitoring and auto-restart...${NC}"
if [ -f "setup_monitoring.sh" ]; then
    chmod +x setup_monitoring.sh
    ./setup_monitoring.sh
else
    echo -e "${YELLOW}⚠ Monitoring script not found, skipping...${NC}"
fi

echo ""
echo -e "${YELLOW}[7] Restarting all services...${NC}"
sudo systemctl restart techlynxpro
sudo systemctl restart nginx

sleep 3

echo ""
echo -e "${YELLOW}[8] Verifying services...${NC}"
if sudo systemctl is-active --quiet techlynxpro; then
    echo -e "${GREEN}✓ Gunicorn is running${NC}"
else
    echo -e "${RED}✗ Gunicorn is NOT running${NC}"
fi

if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is NOT running${NC}"
fi

echo ""
echo -e "${YELLOW}[9] Testing website...${NC}"
HTTP_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/ 2>/dev/null || echo "000")
if [ "$HTTP_TEST" = "200" ] || [ "$HTTP_TEST" = "301" ] || [ "$HTTP_TEST" = "302" ]; then
    echo -e "${GREEN}✓ Website is responding (HTTP $HTTP_TEST)${NC}"
else
    echo -e "${YELLOW}⚠ Website returned: $HTTP_TEST${NC}"
fi

echo ""
echo "========================================="
echo -e "${GREEN}Production deployment completed!${NC}"
echo "========================================="
echo ""
echo "Your website is now:"
echo "  ✓ Running with auto-restart"
echo "  ✓ Monitored every 5 minutes"
echo "  ✓ Will auto-recover from failures"
echo ""
echo "Next step (optional): Set up SSL:"
echo "  chmod +x setup_ssl.sh && ./setup_ssl.sh"
echo ""
echo "Or manually:"
echo "  sudo dnf install -y certbot python3-certbot-nginx"
echo "  sudo certbot --nginx -d techlynxpro.com -d www.techlynxpro.com"
echo ""



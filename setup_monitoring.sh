#!/bin/bash

# Server Monitoring and Auto-Recovery Setup
# Ensures website stays live all the time

set -e

echo "========================================="
echo "Setting up Server Monitoring"
echo "========================================="
echo ""

PROJECT_DIR="/home/ec2-user/techlynxpro"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[1] Creating health check script...${NC}"
cat > $PROJECT_DIR/health_check.sh << 'EOF'
#!/bin/bash
# Health check script for Techlynx Pro

PROJECT_DIR="/home/ec2-user/techlynxpro"
LOG_FILE="$PROJECT_DIR/health_check.log"

# Check Gunicorn
if ! systemctl is-active --quiet techlynxpro; then
    echo "$(date): Gunicorn is down, restarting..." >> $LOG_FILE
    sudo systemctl restart techlynxpro
    sleep 5
fi

# Check Nginx
if ! systemctl is-active --quiet nginx; then
    echo "$(date): Nginx is down, restarting..." >> $LOG_FILE
    sudo systemctl restart nginx
    sleep 5
fi

# Check if website is responding
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/ 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ] && [ "$HTTP_CODE" != "301" ] && [ "$HTTP_CODE" != "302" ]; then
    echo "$(date): Website not responding (HTTP $HTTP_CODE), restarting services..." >> $LOG_FILE
    sudo systemctl restart techlynxpro
    sudo systemctl restart nginx
    sleep 10
    
    # Check again
    HTTP_CODE2=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/ 2>/dev/null || echo "000")
    if [ "$HTTP_CODE2" != "200" ] && [ "$HTTP_CODE2" != "301" ] && [ "$HTTP_CODE2" != "302" ]; then
        echo "$(date): Website still not responding after restart (HTTP $HTTP_CODE2)" >> $LOG_FILE
    fi
fi
EOF

chmod +x $PROJECT_DIR/health_check.sh
echo -e "${GREEN}✓ Health check script created${NC}"

echo ""
echo -e "${YELLOW}[2] Setting up systemd timer for health checks...${NC}"
sudo tee /etc/systemd/system/techlynxpro-healthcheck.service > /dev/null << 'EOFSERVICE'
[Unit]
Description=Techlynx Pro Health Check
After=network.target

[Service]
Type=oneshot
User=ec2-user
ExecStart=/home/ec2-user/techlynxpro/health_check.sh
EOFSERVICE

sudo tee /etc/systemd/system/techlynxpro-healthcheck.timer > /dev/null << 'EOFTIMER'
[Unit]
Description=Run Techlynx Pro Health Check every 5 minutes
Requires=techlynxpro-healthcheck.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min
Unit=techlynxpro-healthcheck.service

[Install]
WantedBy=timers.target
EOFTIMER

sudo systemctl daemon-reload
sudo systemctl enable techlynxpro-healthcheck.timer
sudo systemctl start techlynxpro-healthcheck.timer

echo -e "${GREEN}✓ Health check timer enabled (runs every 5 minutes)${NC}"

echo ""
echo -e "${YELLOW}[3] Improving Gunicorn service for auto-restart...${NC}"
sudo tee /etc/systemd/system/techlynxpro.service > /dev/null << 'EOFSERVICE'
[Unit]
Description=Techlynx Pro Gunicorn daemon
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/techlynxpro
Environment="PATH=/home/ec2-user/techlynxpro/venv/bin"
ExecStart=/home/ec2-user/techlynxpro/venv/bin/gunicorn \
    --config /home/ec2-user/techlynxpro/gunicorn_config.py \
    techlynx_project.wsgi:application

Restart=always
RestartSec=3
StartLimitInterval=0
StartLimitBurst=0

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=techlynxpro

[Install]
WantedBy=multi-user.target
EOFSERVICE

sudo systemctl daemon-reload
sudo systemctl enable techlynxpro
sudo systemctl restart techlynxpro

echo -e "${GREEN}✓ Gunicorn service improved with auto-restart${NC}"

echo ""
echo -e "${YELLOW}[4] Setting up log rotation...${NC}"
sudo tee /etc/logrotate.d/techlynxpro > /dev/null << 'EOFLOGROTATE'
/home/ec2-user/techlynxpro/health_check.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
EOFLOGROTATE

echo -e "${GREEN}✓ Log rotation configured${NC}"

echo ""
echo -e "${YELLOW}[5] Testing services...${NC}"
sleep 2

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

if sudo systemctl is-active --quiet techlynxpro-healthcheck.timer; then
    echo -e "${GREEN}✓ Health check timer is active${NC}"
else
    echo -e "${RED}✗ Health check timer is NOT active${NC}"
fi

echo ""
echo "========================================="
echo -e "${GREEN}Monitoring setup completed!${NC}"
echo "========================================="
echo ""
echo "Features enabled:"
echo "  ✓ Auto-restart on failure"
echo "  ✓ Health check every 5 minutes"
echo "  ✓ Automatic service recovery"
echo "  ✓ Log rotation"
echo ""
echo "Check status:"
echo "  sudo systemctl status techlynxpro"
echo "  sudo systemctl status techlynxpro-healthcheck.timer"
echo "  tail -f $PROJECT_DIR/health_check.log"
echo ""



#!/bin/bash
# Renew Let's Encrypt SSL for techlynxpro.com (run on the EC2/server as root/sudo).
# Fixes browser warning: net::ERR_CERT_DATE_INVALID / "Your connection is not private"

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="/home/ec2-user/techlynxpro"
NGINX_CONF="/etc/nginx/conf.d/techlynxpro.conf"

echo "========================================="
echo "SSL certificate renewal — techlynxpro.com"
echo "========================================="
echo ""

echo -e "${YELLOW}[1] Ensure ACME webroot exists (HTTP-01 challenge)...${NC}"
sudo mkdir -p /var/www/certbot/.well-known/acme-challenge
sudo chown -R nginx:nginx /var/www/certbot 2>/dev/null || sudo chown -R ec2-user:ec2-user /var/www/certbot

echo -e "${YELLOW}[2] Deploy nginx config (must NOT redirect /.well-known/acme-challenge/)...${NC}"
if [ -f "$PROJECT_DIR/nginx/techlynxpro.conf" ]; then
    sudo cp "$PROJECT_DIR/nginx/techlynxpro.conf" "$NGINX_CONF"
fi
sudo nginx -t
sudo systemctl reload nginx

echo -e "${YELLOW}[3] Renew or re-issue certificate...${NC}"
if sudo certbot renew --quiet --deploy-hook "systemctl reload nginx"; then
    echo -e "${GREEN}✓ Certificate renewed via certbot renew${NC}"
else
    echo -e "${YELLOW}  renew failed — forcing new certificate (webroot)...${NC}"
    sudo certbot certonly --webroot \
        -w /var/www/certbot \
        -d techlynxpro.com \
        -d www.techlynxpro.com \
        --non-interactive \
        --agree-tos \
        --email admin@techlynxpro.com \
        --force-renewal
fi

echo -e "${YELLOW}[4] Reload nginx with new certificate...${NC}"
sudo nginx -t
sudo systemctl reload nginx

echo -e "${YELLOW}[5] Enable automatic renewal timer...${NC}"
sudo systemctl enable certbot-renew.timer 2>/dev/null || true
sudo systemctl start certbot-renew.timer 2>/dev/null || true

echo ""
echo -e "${YELLOW}[6] Certificate status:${NC}"
sudo certbot certificates || true

echo ""
echo "Test from server:"
curl -sI --connect-timeout 10 https://techlynxpro.com/ | head -n 5 || true

echo ""
echo "========================================="
echo -e "${GREEN}SSL renewal complete.${NC}"
echo "Open https://techlynxpro.com in a private window to verify."
echo "========================================="

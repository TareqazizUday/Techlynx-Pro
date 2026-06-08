#!/bin/bash

# SSL Certificate Setup Script
# Run this on your server

set -e

echo "========================================="
echo "Setting up SSL Certificate"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}[1] Installing Certbot...${NC}"
sudo dnf install -y certbot python3-certbot-nginx

echo ""
echo -e "${YELLOW}[2] Obtaining SSL certificate...${NC}"
echo "This will ask for your email address and agree to terms."
echo ""

sudo mkdir -p /var/www/certbot/.well-known/acme-challenge
sudo chown -R nginx:nginx /var/www/certbot 2>/dev/null || sudo chown -R ec2-user:ec2-user /var/www/certbot

# Deploy nginx with ACME exception before certbot (see nginx/techlynxpro.conf)
if [ -f nginx/techlynxpro.conf ]; then
    sudo cp nginx/techlynxpro.conf /etc/nginx/conf.d/techlynxpro.conf
    sudo nginx -t && sudo systemctl reload nginx
fi

sudo certbot --nginx -d techlynxpro.com -d www.techlynxpro.com --non-interactive --agree-tos --email admin@techlynxpro.com --redirect

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSL certificate installed successfully!${NC}"
else
    echo -e "${RED}✗ SSL certificate installation failed${NC}"
    echo "Try webroot: sudo certbot certonly --webroot -w /var/www/certbot -d techlynxpro.com -d www.techlynxpro.com"
    exit 1
fi

echo ""
echo -e "${YELLOW}[3] Enabling automatic renewal timer...${NC}"
sudo systemctl enable certbot-renew.timer 2>/dev/null || true
sudo systemctl start certbot-renew.timer 2>/dev/null || true

echo ""
echo -e "${YELLOW}[4] Testing certificate renewal...${NC}"
sudo certbot renew --dry-run

echo ""
echo -e "${YELLOW}[5] Restarting Nginx...${NC}"
sudo systemctl restart nginx

echo ""
echo "========================================="
echo -e "${GREEN}SSL setup completed!${NC}"
echo "========================================="
echo ""
echo "Your website is now available at:"
echo "  ✓ https://techlynxpro.com"
echo "  ✓ https://www.techlynxpro.com"
echo ""
echo "HTTP will automatically redirect to HTTPS"
echo ""



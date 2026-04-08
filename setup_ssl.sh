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

sudo certbot --nginx -d techlynxpro.com -d www.techlynxpro.com --non-interactive --agree-tos --email admin@techlynxpro.com --redirect

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSL certificate installed successfully!${NC}"
else
    echo -e "${RED}✗ SSL certificate installation failed${NC}"
    echo "Please run manually: sudo certbot --nginx -d techlynxpro.com -d www.techlynxpro.com"
    exit 1
fi

echo ""
echo -e "${YELLOW}[3] Testing certificate renewal...${NC}"
sudo certbot renew --dry-run

echo ""
echo -e "${YELLOW}[4] Restarting Nginx...${NC}"
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



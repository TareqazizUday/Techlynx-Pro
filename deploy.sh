#!/bin/bash

# Techlynx Pro Deployment Script
# Run this script on your EC2 server to deploy the application

set -e  # Exit on error

echo "========================================="
echo "Techlynx Pro Deployment Script"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as ec2-user
if [ "$USER" != "ec2-user" ]; then
    echo -e "${YELLOW}Warning: Not running as ec2-user. Some commands may need sudo.${NC}"
fi

# Project directory
PROJECT_DIR="/home/ec2-user/techlynxpro"
VENV_DIR="$PROJECT_DIR/venv"

echo -e "${GREEN}Step 1: Installing system dependencies...${NC}"
sudo dnf update -y
sudo dnf install -y python3.11 python3.11-pip python3.11-devel nginx git

echo -e "${GREEN}Step 2: Creating project directory...${NC}"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo -e "${GREEN}Step 3: Creating virtual environment...${NC}"
python3.11 -m venv venv
source venv/bin/activate

echo -e "${GREEN}Step 4: Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}Step 5: Setting up environment variables...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    # Generate secret key automatically
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key)")
    cat > .env << EOF
# Django Settings
SECRET_KEY=$SECRET_KEY
DEBUG=False

# Gemini API (Optional)
GEMINI_API_KEY=
EOF
    echo -e "${GREEN}✓ .env file created with auto-generated SECRET_KEY${NC}"
else
    echo -e "${GREEN}.env file already exists.${NC}"
    # Check if SECRET_KEY is set, if not generate one
    if ! grep -q "SECRET_KEY=" .env || grep -q "SECRET_KEY=your-secret-key" .env; then
        echo -e "${YELLOW}Generating new SECRET_KEY...${NC}"
        SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key)")
        if grep -q "SECRET_KEY=" .env; then
            sed -i "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" .env
        else
            echo "SECRET_KEY=$SECRET_KEY" >> .env
        fi
        echo -e "${GREEN}✓ SECRET_KEY updated${NC}"
    fi
    # Ensure DEBUG is False
    if grep -q "DEBUG=True" .env; then
        sed -i "s|DEBUG=True|DEBUG=False|" .env
        echo -e "${GREEN}✓ DEBUG set to False${NC}"
    fi
fi

echo -e "${GREEN}Step 6: Running migrations...${NC}"
source venv/bin/activate
python manage.py migrate

echo -e "${GREEN}Step 7: Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}Step 8: Creating necessary directories...${NC}"
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R ec2-user:ec2-user /var/log/gunicorn
sudo chown -R ec2-user:ec2-user /var/run/gunicorn

echo -e "${GREEN}Step 9: Setting up systemd service...${NC}"
sudo cp systemd/techlynxpro.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable techlynxpro
sudo systemctl start techlynxpro

echo -e "${GREEN}Step 10: Setting up Nginx...${NC}"
sudo cp nginx/techlynxpro.conf /etc/nginx/conf.d/
sudo nginx -t  # Test configuration
sudo systemctl enable nginx
sudo systemctl restart nginx

echo -e "${GREEN}Step 11: Configuring firewall...${NC}"
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${YELLOW}Checking services status...${NC}"
sleep 2
sudo systemctl status techlynxpro --no-pager -l | head -10
echo ""
sudo systemctl status nginx --no-pager -l | head -10
echo ""
echo -e "${GREEN}✓ All services are running!${NC}"
echo ""
echo "Next steps (optional):"
echo "1. Create superuser: cd $PROJECT_DIR && source venv/bin/activate && python manage.py createsuperuser"
echo "2. View logs: sudo journalctl -u techlynxpro -f"
echo "3. Set up SSL certificate: sudo dnf install -y certbot python3-certbot-nginx && sudo certbot --nginx -d techlynxpro.com -d www.techlynxpro.com"
echo ""
echo -e "${GREEN}Your site should be accessible at: http://techlynxpro.com${NC}"
echo -e "${GREEN}Admin panel: http://techlynxpro.com/admin/${NC}"
echo ""

